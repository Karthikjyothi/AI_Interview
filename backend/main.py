import sys
import os
from unittest import result

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, UploadFile, File, WebSocket, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pypdf import PdfReader

from utils.analyze_candidate import analyze_candidate_response_and_generate_new_question
from utils.basic_details import get_ai_greeting_message
from utils.coding.question_generator import generate_coding_question
from utils.technical.question_generator import generate_technical_question
from utils.technical.evaluator import evaluate_technical_answer
from utils.technical.followup_generator import generate_followup_question

from resume_analyzer.analyzer import analyze_resume_data
from database import cursor, conn

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from pydantic import BaseModel
import subprocess
import tempfile
import uuid
import os

from coding_testcases import HIDDEN_TESTS

CURRENT_MOCK_CACHE = None

# ================= GLOBAL STATE =================
interview_data = {"answers": [], "scores": [], "feedbacks": []}
technical_scores = []
coding_round = 0
max_coding_questions = 0
cheating_scores = {}
question_count = 0
question_index = 0
conversation_history = []
available_projects = []
current_project_q_count = 0


def extract_skills_from_resume(text):
    text = text.lower()

    skill_keywords = [
        "python", "java", "react", "node", "sql",
        "machine learning", "ai", "data structures",
        "algorithms", "dbms", "os", "networking"
    ]

    skills = [skill for skill in skill_keywords if skill in text]

    return skills if skills else ["programming"]

import random

def generate_question_from_skill(skill):
    templates = [
        f"Can you walk me through a project where you used {skill}?",
        f"What challenges have you faced while working with {skill}?",
        f"How would you explain {skill} to a beginner?",
        f"In your experience, what are the strengths and limitations of {skill}?",
        f"How have you applied {skill} in real-world scenarios?",
        f"What improvements would you make if you revisit your work with {skill}?",
        f"Can you compare {skill} with another technology you know?",
        f"What are common mistakes developers make when using {skill}?"
    ]

    return random.choice(templates)

def generate_project_question(project):
    templates = [
        f"Can you explain your project: {project}?",
        f"What was the main objective of {project}?",
        f"What challenges did you face while working on {project}?",
        f"What technologies did you use in {project} and why?",
        f"If you had more time, how would you improve {project}?",
        f"What was your role in {project}?",
        f"What did you learn from working on {project}?"
    ]

    return random.choice(templates)

import re

def extract_projects_from_resume(text):
    import re

    if not text:
        return []

    lines = text.split("\n")
    projects = []

    for i, line in enumerate(lines):
        line_lower = line.lower().strip()

        # detect project section
        if "project" in line_lower:

            # take next few lines as project names
            for j in range(i + 1, min(i + 6, len(lines))):
                candidate = lines[j].strip()

                # clean text
                candidate = re.sub(r"[^a-zA-Z0-9\s]", "", candidate)

                # ignore empty / small / generic
                if (
                    len(candidate) > 5
                    and "project" not in candidate.lower()
                    and candidate.lower() not in ["projects", "academic projects"]
                ):
                    projects.append(candidate)

    return list(set(projects))[:7]
# ================= APP =================
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


app.mount("/files", StaticFiles(directory="."), name="files")
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"] # 👈 Add this line!
)

# ================= MODELS =================
class InterviewRequest(BaseModel):
    question: str
    answer: str
    job_description: str
    resume_highlights: str = ""
    mode: str
    num_questions: int = 5
    total_questions: int = 5


# Create the High-Capacity Mock Test Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mock_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        section TEXT,        -- 'Numerical', 'Verbal', 'Reasoning', 'Coding'
        q_type TEXT,         -- 'mcq' or 'coding'
        question TEXT,
        option_a TEXT,       -- Null for coding
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_answer TEXT, -- Index (0-3) or Sample Logic for coding
        points INTEGER DEFAULT 1
    )
''')
conn.commit()

# ================= HOME =================
@app.get("/")
def home():
    return {"message": "Backend running"}

# ================= MOCK TEST CONFIG =================
LIMITS = {
    "Numerical": 10,
    "Verbal": 15,
    "Reasoning": 10,
    "Advanced quants & reasoning": 10,
    "Coding": 2
}

# ================= MOCK TEST API =================
@app.get("/get-mock-test")
async def get_mock_test():
    print("🔥 NEW MOCK TEST API CALLED")
    global CURRENT_MOCK_CACHE

    if CURRENT_MOCK_CACHE:
        print("USING CACHED MOCK TEST")
        return CURRENT_MOCK_CACHE

    exam_structure = {}

    # ================= CODING FROM DB FIRST =================
    cursor.execute("""
        SELECT * FROM mock_questions
        WHERE section='Coding'
        ORDER BY RANDOM()
        LIMIT 2
    """)
    rows = cursor.fetchall()

    exam_structure["Coding"] = [
        {
            "id": r[0],
            "type": r[3],
            "question": r[4],
            "options": [],
            "correct": r[9]
        }
        for r in rows
    ]


    # ================= SINGLE MASTER AI CALL =================
    try:
        difficulty = "Medium"

        prompt = f"""
        You are an expert TCS NQT exam paper setter.

        You MUST generate a COMPLETE TCS NQT mock exam in ONE valid JSON response.

        ALL sections are COMPULSORY.
        Do not skip any section.
        Do not stop until all sections are fully generated.

        MANDATORY COUNT:
        Generate a FULL TCS NQT mock exam with:
        - 10 HIGH-QUALITY {difficulty} level Numerical questions
        - 15 HIGH-QUALITY {difficulty} level Verbal questions
        - 10 HIGH-QUALITY {difficulty} level Reasoning questions
        - 10 HIGH-QUALITY {difficulty} level Advanced quants & reasoning questions

        If any section has fewer questions, the response is invalid.


        STRICT RULES:
        - Questions must match real TCS NQT difficulty (not basic like 2+2)
        - Avoid trivial questions
        - Include logical reasoning, tricky calculations, or real-world scenarios
        - Ensure options are confusing but valid
        - Only 1 correct answer

        FORMAT (VERY IMPORTANT):
        Return ONLY JSON object like this:

        {{
            "Numerical": [
                {{
                    "type": "mcq",
                    "question": "Question text",
                    "options": ["A", "B", "C", "D"],
                    "correct": "0"
                }}
            ],
            "Verbal": [],
            "Reasoning": [],
            "Advanced quants & reasoning": [],
            "Coding": []
        }}

        SECTION RULES:
        - Generate questions that require multiple steps of reasoning or calculation.
        - Select topics in a random order, but ensure a good mix of all important TCS NQT topics. don't generate same questions everytime
        Numerical:
        - Time-speed-distance
        - Profit & loss
        - Percentages
        - Ratios
        - Averages
        - Number System
        - Simple & Compound Interest
        - Time & Work
        - Time-Speed-Distance
        - Data Interpretation (Graphs, Charts)
        - Probability 
        - Mensuration
        - Simplification

        Verbal:
        - Reading comprehension
        - Sentence correction
        - Vocabulary (advanced)
        - Synonyms
        - Antonyms
        - Error Correction (Grammar)
        - Sentence Rearrangement
        - Paragraph Completion
        - Prepositions
        - Tenses

        Reasoning:
        - Number series
        - Coding-decoding
        - Logical puzzles
        - Blood relations
        - Seating Arrangements
        - Direction sense
        - Syllogism

        Advanced quants & reasoning:
        - Higher difficulty level of all the above topics

        Coding:
        - Data Structures (Arrays, Linked Lists, Stacks, Queues), Algorithms (Sorting/Searching), Strings, Number Theory, Matrix operations.
        - Ask 1 problem only (if section is Coding) from the above points but make it tricky and not a common one like "reverse a string". Focus on problem-solving and logic also try to extract some context from the question to make it more real-world like. For example, if it's a string problem, embed it in a real-world scenario like "You are building a search engine and need to optimize string matching for user queries. Write a function that...".
        - Also give few examples of input and output for the coding question to make it more clear. Make sure the problem is of medium difficulty level and not too easy.
        - Give testcases for the coding question in the correct_answer field in a structured format like: input hjgh, output 2, input abc, output 3, etc. This will be used for auto-evaluation later.
        - Medium DSA level

        IMPORTANT:
        Do NOT generate easy questions.
        Make them slightly tricky like real placement exams.
        """

        ai_data = call_groq_llm(prompt)
        print("MASTER AI RESPONSE:", ai_data)

        if isinstance(ai_data, dict):
            normalized = {k.lower(): v for k, v in ai_data.items()}

            exam_structure["Numerical"] = normalized.get("numerical", [])
            exam_structure["Verbal"] = normalized.get("verbal", [])
            exam_structure["Reasoning"] = normalized.get("reasoning", [])
            exam_structure["Advanced quants & reasoning"] = normalized.get("advanced quants & reasoning", [])
            if normalized.get("coding"):
                exam_structure["Coding"] = normalized.get("coding", [])

        else:
            exam_structure["Numerical"] = []
            exam_structure["Verbal"] = []
            exam_structure["Reasoning"] = []
            exam_structure["Advanced quants & reasoning"] = []
            exam_structure["Coding"] = []
    except Exception as e:
        print("MASTER AI FAILED:", e)
        exam_structure["Numerical"] = []
        exam_structure["Verbal"] = []
        exam_structure["Reasoning"] = []
        exam_structure["Advanced quants & reasoning"] = []

    # ================= VALIDATE AI QUESTIONS =================
    cleaned = {
        "Numerical": [],
        "Verbal": [],
        "Reasoning": [],
        "Advanced quants & reasoning": [],
        "Coding": exam_structure["Coding"]
    }

    for sec in ["Numerical", "Verbal", "Reasoning", "Advanced quants & reasoning"]:
        data_list = exam_structure.get(sec, [])

        valid_ai = []

        for i, q in enumerate(data_list):
            try:
                question = q.get("question") or q.get("ques")
                options = q.get("options") or []

                if question and isinstance(options, list) and len(options) >= 4:
                    valid_ai.append({
                        "id": f"ai-{sec}-{i}",
                        "type": "mcq",
                        "question": question,
                        "options": options[:4]
                    })
            except:
                continue

        # coding preserve directly
        coding_ai = []
        for i, q in enumerate(exam_structure.get("Coding", [])):
            coding_ai.append({
                "id": q.get("id", f"code-{i}"),
                "type": "coding",
                "question": q.get("question", ""),
                "options": [],
                "correct": q.get("correct", "")
            })
            
        cleaned["Coding"] = coding_ai
        cleaned[sec] = valid_ai

    # ================= FORCE EXACT COUNTS =================
    for sec, limit in LIMITS.items():

        current_count = len(cleaned.get(sec, []))

        if current_count > limit:
            cleaned[sec] = cleaned[sec][:limit]

        elif current_count < limit:

            needed = limit - current_count

            db_sec = sec
            if sec == "Advanced quants & reasoning":
                db_sec = "Advanced quants & reasoning"

            cursor.execute("""
                SELECT * FROM mock_questions
                WHERE LOWER(section)=LOWER(?)
                ORDER BY RANDOM()
                LIMIT ?
            """, (db_sec, needed))

            rows = cursor.fetchall()

            extra_questions = [
                {
                    "id": r[0],
                    "type": r[3],
                    "question": r[4],
                    "options": [r[5], r[6], r[7], r[8]] if r[3] == "mcq" else [],
                    "correct": r[9] if len(r) > 9 else ""
                }
                for r in rows
            ]

            cleaned[sec].extend(extra_questions)

    print("FINAL CLEANED:")
    for k, v in cleaned.items():
        print(k, "→", len(v))

    CURRENT_MOCK_CACHE = cleaned
    return cleaned

# ================= START =================
@app.post("/start")
def start_interview(name: str, resume_text: str = ""): # Pass resume_text if available
    global technical_scores, coding_round, question_count, available_projects, current_project_q_count
    
    technical_scores = []
    coding_round = 0
    current_project_q_count = 0
    max_coding_questions = 0
    global question_count
    question_count = 0
    global question_index
    question_index = 0
    
    # 🔥 Initialize and shuffle projects so it's random every time
    if resume_text:
        available_projects = extract_projects_from_resume(resume_text)
        random.shuffle(available_projects) 
    
    return {"question": get_ai_greeting_message(name)}

# ================= WEBSOCKET =================
@app.websocket("/ws/{candidate_id}")
async def websocket_endpoint(websocket: WebSocket, candidate_id: str):
    await websocket.accept()
    cheating_scores[candidate_id] = 0

    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event")

            if event == "TAB_SWITCH":
                cheating_scores[candidate_id] += 2
            elif event == "SCREEN_STOP":
                cheating_scores[candidate_id] += 5
            elif event == "LOOK_AWAY":
                cheating_scores[candidate_id] += 1
            elif event == "MULTIPLE_FACES":
                cheating_scores[candidate_id] += 3
            elif event == "NO_FACE":
                cheating_scores[candidate_id] += 2

            await websocket.send_json({
                "cheating_score": cheating_scores[candidate_id]
            })
    except:
        print("WebSocket disconnected")

# ================= RESUME UPLOAD =================
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(file_location)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return {"resume_text": text[:5000]}

# ================= NEXT QUESTION =================
@app.post("/next-question")
async def next_question(data: InterviewRequest):

    global technical_scores, coding_round, max_coding_questions
    global question_count
    question_count += 1

    # 🔥 SAFETY INPUTS
    data.question = data.question or "Tell me about yourself"
    data.answer = data.answer or "No answer"
    data.resume_highlights = data.resume_highlights or ""
    data.job_description = data.job_description or "Software Engineer"

    if len(data.answer.strip()) < 10:
        return {
            "type": "technical",
            "next_question": "Please provide a more detailed answer.",
            "feedback": {"score": 0, "feedback": "Answer too short"}
        }

    projects = extract_projects_from_resume(data.resume_highlights)
    skills = extract_skills_from_resume(data.resume_highlights)

    try:
        # ================= TECH MODE =================
        # ================= TECH MODE =================
        if data.mode == "technical":
            global available_projects, current_project_q_count
            
            try:
                feedback = await evaluate_technical_answer(str(data.question), str(data.answer))
            except:
                feedback = {"score": 5, "feedback": "Evaluation fallback"}

            # 🛡️ SAFE SCORE EXTRACTION
            if isinstance(feedback, dict):
                score = float(feedback.get("score", 5))
            else:
                # If feedback is just a string, we assume a neutral score
                score = 5.0
                feedback = {"score": 5.0, "feedback": str(feedback)}

            technical_scores.append(score)
            
            # Save for PDF
            interview_data["answers"].append(data.answer)
            interview_data["scores"].append(score)
            interview_data["feedbacks"].append(feedback.get("feedback", ""))

            # 🧠 SMART QUESTION LOGIC
            if question_count < data.total_questions:
                
                # 🛑 EVEN QUESTIONS (2, 4, 6...): Core Fundamentals
                if question_count % 2 == 0:
                    core_topics = ["DSA", "OOPS", "DBMS", "Computer Networks", "Operating Systems"]
                    selected_topic = random.choice(core_topics)
                    next_q = generate_technical_question(selected_topic, "Focus on core theory and fundamentals and don't ask too difficult questions about the core topics. focus on understanding candidate's depth of knowledge in core subjects.")
                
                # 🚀 ODD QUESTIONS (1, 3, 5...): AI Project Deep-Dive
                else:
                    # Initialize projects if list is empty
                    if not available_projects and data.resume_highlights:
                        available_projects = extract_projects_from_resume(data.resume_highlights)
                        random.shuffle(available_projects)

                    # Rotation Logic: Move to next project after 2 questions
                    if available_projects and current_project_q_count >= 2:
                        available_projects.pop(0)
                        current_project_q_count = 0

                    if available_projects:
                        target_project = available_projects[0]
                        current_project_q_count += 1
                        context = f"Candidate project: {target_project}. Ask a deep technical question about the implementation or challenges."
                    else:
                        context = f"Candidate skills: {data.resume_highlights}. Ask about a specific technical skill."

                    try:
                        # Call your AI generator
                        next_q = generate_technical_question(data.job_description, context)
                    except:
                        # Real-world fallback (not a generic template)
                        next_q = f"I see you worked on {available_projects[0] if available_projects else 'technical projects'}. Can you explain the most difficult bug you solved there?"

                return {
                    "type": "technical",
                    "next_question": str(next_q),
                    "feedback": feedback
                }
            
            # Transition to Coding
            if coding_round < 1:  # Change to 2 if you want two coding questions
                coding_round += 1
                try:
                    next_q = generate_coding_question(data.job_description, data.resume_highlights)
                except:
                    next_q = "Write a code to find the maximum element in a list."
                
                return {
                    "type": "coding", # 🔥 This tells React to show the Code Editor
                    "next_question": str(next_q),
                    "feedback": feedback
                }

            # 🏁 STEP 3: ONLY END AFTER CODING IS DONE
            return {
                "type": "end",
                "next_question": "Technical and Coding rounds completed! Well done.",
                "feedback": feedback
            }

            return {"type": "end", "next_question": "Interview completed", "feedback": feedback}

            # 🏁 END INTERVIEW
            return {
                "type": "end",
                "next_question": "Interview completed successfully. You can now download your report.",
                "feedback": feedback
            }

        # ================= HR MODE =================
        else:
            try:
                next_q, feedback = await analyze_candidate_response_and_generate_new_question(
                    data.question,
                    data.answer,
                    data.job_description,
                    data.resume_highlights
                )
            except:
                next_q = "Tell me about yourself."
                feedback = {"score": 5, "feedback": "Fallback HR"}

            if isinstance(feedback, dict):
                score = float(feedback.get("score", 5))
            else:
                score = 5.0
                feedback = {"score": score, "feedback": str(feedback)}

            return {
                "type": "hr",
                "next_question": str(next_q),
                "feedback": feedback
            }

    except Exception as e:
        print("🔥 RECOVERY LOGIC TRIGGERED:", e)
        
        # Instead of using generic templates, let's try a smarter fallback
        if available_projects:
            target = available_projects[0]
            next_q = f"Looking at your {target} project, what was the most difficult technical hurdle you had to overcome?"
        else:
            next_q = "Can you explain a complex technical problem you've solved recently?"

        return {
            "type": "technical",
            "next_question": next_q,
            "feedback": {"score": 5, "feedback": "System recovered from a processing lag."}
        }

# ================= CODE EVAL =================
@app.post("/evaluate-code")
async def evaluate_code(data: dict):
    code = data.get("code", "")

    score = 0
    if "def" in code: score += 3
    if "return" in code: score += 2
    if "for" in code or "while" in code: score += 2
    if len(code) > 50: score += 3

    return {"score": min(score, 10), "feedback": "Good attempt"}

# ================= ADMIN =================
@app.get("/admin/results")
def get_results():
    cursor.execute("SELECT * FROM results")
    return {"data": cursor.fetchall()}

# ================= PDF =================
def generate_pdf_report():
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("🚀 AI Interview Performance Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    scores = interview_data["scores"]
    avg_score = sum(scores) / len(scores) if scores else 0
    elements.append(Paragraph(f"Overall Interview Score: {avg_score:.2f}/10", styles["Heading2"]))
    elements.append(Spacer(1, 20))

    # Loop through the saved data and add it to the PDF
    for i in range(len(interview_data["answers"])):
        elements.append(Paragraph(f"Question {i+1}:", styles["Heading3"]))
        elements.append(Paragraph(f"Answer: {interview_data['answers'][i]}", styles["Normal"]))
        elements.append(Paragraph(f"Feedback: {interview_data['feedbacks'][i]}", styles["Italic"]))
        elements.append(Spacer(1, 15))

    doc.build(elements)

from fastapi.responses import FileResponse

@app.get("/download-report")
async def download_report():
    generate_pdf_report()  # Your function that creates the actual file
    return FileResponse(
        path="report.pdf", 
        filename="Interview_Report.pdf", 
        media_type="application/pdf"
    )

from fastapi import UploadFile, File, Form
from pypdf import PdfReader
import os

@app.post("/analyze-resume-full")
async def analyze_resume_full(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    target_role: str = Form("Full Stack Developer") # Default if not sent
):
    try:
        # 1. Save File Temporarily
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 2. Extract Text from PDF
        text_content = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text_content += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return {"error": "Could not read PDF content"}

        # 3. 🔥 DYNAMIC GROQ PROMPT (Professional ATS Scoring)
        prompt = f"""
        You are a Professional ATS System. Analyze this resume for the role of {target_role}:
        ---
        resume_short = text_content[:2800]
        ---

        Calculate the 'score' (0-100) using strict weights.
        
        Return ONLY a valid JSON object with EXACTLY this amount of data:
        {{
            "score": int,
            "breakdown": {{
                "role_match": int,
                "impact_metrics": int,
                "skill_depth": int,
                "formatting": int
            }},
            "skills": ["List at least 8-10 technical skills found"],
            "missing_keywords": ["List at least 5-7 specific technical keywords missing"],
            "tips": [
                {{"type": "good", "msg": "Provide at least 7 detailed positive points"}},
                {{"type": "bad", "msg": "Provide at least 7 detailed improvement points"}}
            ],
            "recommendations": [
                "Provide EXACTLY 10 specific course names related to {target_role} and the missing skills"
            ],
            "cand_level": "string",
            "predicted_field": "string"
        }}
        """

        # 4. Call your Groq function
        result = call_groq_llm(prompt)

        # 5. Fallback in case AI fails to return JSON
        result = sanitize_resume_result(result)
        print("FINAL SANITIZED RESUME RESULT:", result)
        # 6. 💾 Save to DB
        cursor.execute(
            "INSERT INTO results (name, email, score, skills) VALUES (?, ?, ?, ?)",
            (name, email, result.get("score", 0), ", ".join(result.get("skills", [])))
        )
        conn.commit()

        # 7. Add User Metadata for Frontend
        result["name"] = name
        result["email"] = email
        result["phone"] = phone

        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)

        return result

    except Exception as e:
        print("🔥 RESUME ERROR:", e)
        return {"error": str(e)}

import os
from groq import Groq
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def call_groq_llm(prompt):
    try:
        print("PROMPT LENGTH:", len(prompt))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI assistant that ALWAYS returns only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            temperature=0.9,
            max_tokens=1400
        )

        raw = chat_completion.choices[0].message.content
        print("RAW GROQ:", raw)

        return json.loads(raw)

    except Exception as e:
        print(f"Groq AI Error: {e}")
        return {}
    
def sanitize_resume_result(result):
    if not isinstance(result, dict):
        result = {}

    breakdown = result.get("breakdown", {})

    return {
        "score": result.get("score", 70),

        "breakdown": {
            "role_match": breakdown.get("role_match", 75),
            "impact_metrics": breakdown.get("impact_metrics", 70),
            "skill_depth": breakdown.get("skill_depth", 65),
            "formatting": breakdown.get("formatting", 80)
        },

        "skills": result.get("skills", [
            "Python", "Java", "SQL", "React", "FastAPI", "DBMS", "Git", "Problem Solving"
        ]),

        "missing_keywords": result.get("missing_keywords", [
            "Docker", "Cloud", "System Design", "Testing", "Deployment"
        ]),

        "tips": result.get("tips", [
            {"type": "good", "msg": "Resume has relevant technical exposure."},
            {"type": "good", "msg": "Candidate profile aligns with software roles."},
            {"type": "good", "msg": "Projects provide practical learning evidence."},
            {"type": "bad", "msg": "Projects need stronger measurable impact metrics."},
            {"type": "bad", "msg": "Resume should include more ATS-rich role keywords."},
            {"type": "bad", "msg": "Add certifications and advanced tools exposure."}
        ]),

        "recommendations": result.get("recommendations", [
            "Advanced DSA Course",
            "Full Stack React + FastAPI Bootcamp",
            "SQL Mastery for Placements",
            "System Design Basics",
            "Cloud Deployment Fundamentals"
        ]),

        "cand_level": result.get("cand_level", "Intermediate"),
        "predicted_field": result.get("predicted_field", "Software Development")
    }
    
    
@app.post("/analyze-resume-dynamic")
async def analyze_dynamic(data: dict):
    resume_text = data.get("resume_text", "")
    
    prompt = f"""
    Analyze this resume text for a Software Engineering role:
    ---
    {resume_text[:3000]}
    ---
    Tasks:
    1. Provide a 'Total Score' (0-100) based on content quality.
    2. Check for these sections: Objective, Education, Experience, Internships, Skills, Hobbies, Interests, Achievements, Certifications, Projects.
    3. List 5 'Missing Keywords' to improve the ATS ranking.
    4. Provide 2 'Course Recommendations' based on the candidate's field.

    Return ONLY a JSON object with this structure:
    {{
        "total_score": int,
        "analysis": {{
            "Section Name": {{"found": bool, "score": int}}
        }},
        "missing_keywords": ["str"],
        "recommended_courses": ["str"],
        "ai_advice": "A short professional tip"
    }}
    """
    
    return call_groq_llm(prompt)

@app.post("/ai-resume-builder")
async def build_resume_entry(data: dict):
    description = data.get("description", "")
    
    prompt = f"""
    Rewrite this simple project description into ONE professional resume bullet point 
    using the STAR method (Action Verb + Task + Result):
    "{description}"
    
    Return ONLY a JSON object: {{"bullet_point": "string"}}
    """
    
    return call_groq_llm(prompt)

@app.delete("/admin/clear-data")
async def clear_data():
    try:
        cursor.execute("DELETE FROM results")
        conn.commit()
        return {"message": "All data cleared successfully"}
    except Exception as e:
        return {"error": str(e)}
    
# --- FETCH TCS EXAM QUESTIONS ---
@app.get("/get-tcs-exam")
async def get_tcs_exam():
    sections = ["Numerical", "Verbal", "Reasoning", "Coding"]
    exam_structure = {}
    
    for sec in sections:
        # We use UPPERCASE/LOWERCASE exactly as it is in seed_question.py
        cursor.execute(
            "SELECT * FROM mock_questions WHERE LOWER(section) = LOWER(?) ORDER BY RANDOM() LIMIT ?",
            (sec, limit)
        )
        rows = cursor.fetchall()
        print(f"DEBUG: Section {sec} found {len(rows)} rows") 
        # If no questions found for a section, return an empty list instead of crashing
        exam_structure[sec] = [
            {
                "id": r[0],
                "type": r[3],
                "question": r[4],
                "options": [r[5], r[6], r[7], r[8]] if r[3] == 'mcq' else [],
                "correct": r[9]
            } for r in rows
        ]
    
    # DEBUG PRINT: Look at your terminal to see if questions are actually found
    print(f"DEBUG: Found {len(exam_structure['Numerical'])} Numerical questions")
    print(f"DEBUG: Found {len(exam_structure['Verbal'])} Verbal questions")
    print(f"DEBUG: Found {len(exam_structure['Reasoning'])} Reasoning questions")
    print(f"DEBUG: Found {len(exam_structure['Coding'])} Coding questions")
    return exam_structure

@app.post("/submit-mock-test")
async def submit_mock_test(data: dict):
    user_answers = data.get("answers", {})

    score = 0
    total = 0
    detailed_result = []

    section_total = {}
    section_score = {}

    for q_id, user_ans in user_answers.items():
        cursor.execute(
            "SELECT section, correct_answer, points FROM mock_questions WHERE id = ?",
            (q_id,)
        )
        row = cursor.fetchone()

        if row:
            section, correct_ans, points = row

            total += points
            section_total[section] = section_total.get(section, 0) + points

            is_correct = str(user_ans) == str(correct_ans)

            if is_correct:
                score += points
                section_score[section] = section_score.get(section, 0) + points

            detailed_result.append({
                "question_id": q_id,
                "section": section,
                "correct": correct_ans,
                "your_answer": user_ans,
                "is_correct": is_correct
            })

    return {
        "score": score,
        "total": total,
        "percentage": (score / total * 100) if total else 0,
        "details": detailed_result,
        "section_total": section_total,
        "section_score": section_score
    }

@app.post("/start-mock-test")
async def start_mock_test():
    return {
        "message": "Mock test started",
        "duration": 90,  # minutes
        "sections": ["Numerical", "Verbal", "Reasoning", "Coding"]
    }

# ================= MOCK FEEDBACK =================
@app.post("/mock-feedback")
async def mock_feedback(data: dict):
    wrong_questions = data.get("wrong_questions", [])

    prompt = f"""
    Analyze these incorrect answers and give improvement tips:
    {wrong_questions}
    """

    return call_groq_llm(prompt)

# ============================================
# CODING ROUND COMPILER ENGINE
# ============================================

class CodeRequest(BaseModel):
    language: str
    code: str
    stdin: str = ""
    keyword: str = ""


def execute_code(language, code, stdin_data=""):
    if language == "java":
        filename = "Main.java"
        filepath = os.path.join(tempfile.gettempdir(), filename)
    ext_map = {
        "python": ".py",
        "cpp": ".cpp",
        "c": ".c",
        "java": ".java",
        "javascript": ".js"
    }

    filename = f"temp_{uuid.uuid4().hex}{ext_map[language]}"
    filepath = os.path.join(tempfile.gettempdir(), filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        # ---------------- PYTHON ----------------
        if language == "python":
            cmd = ["python", filepath]

        # ---------------- JAVASCRIPT ----------------
        elif language == "javascript":
            cmd = ["node", filepath]

        # ---------------- C++ ----------------
        elif language == "cpp":
            exe = filepath.replace(".cpp", ".exe")
            compile_process = subprocess.run(
                ["g++", filepath, "-o", exe],
                capture_output=True,
                text=True
            )
            if compile_process.stderr:
                return compile_process.stderr
            cmd = [exe]

        # ---------------- C ----------------
        elif language == "c":
            exe = filepath.replace(".c", ".exe")
            compile_process = subprocess.run(
                ["gcc", filepath, "-o", exe],
                capture_output=True,
                text=True
            )
            if compile_process.stderr:
                return compile_process.stderr
            cmd = [exe]

        # ---------------- JAVA ----------------
        elif language == "java":
            classname = "Main"

            import re
            code = re.sub(r'public\s+class\s+\w+', 'public class Main', code)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)

            compile_process = subprocess.run(
                ["javac", filepath],
                capture_output=True,
                text=True
            )

            if compile_process.stderr:
                return compile_process.stderr

            cmd = ["java", "-cp", tempfile.gettempdir(), classname]

        # ---------------- RUN FINAL ----------------
        result = subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.stdout.strip():
            return result.stdout.strip()
        else:
            return result.stderr.strip()

    except Exception as e:
        return str(e)


# ---------------- RUN CODE API ----------------
@app.post("/run-code")
def run_code(req: CodeRequest):
    output = execute_code(req.language, req.code, req.stdin)
    return {"output": output}

# ---------------- SUBMIT CODE API ----------------
@app.post("/submit-code")
def submit_code(req: CodeRequest):
    tests = HIDDEN_TESTS.get(req.keyword, [])

    if not tests:
        return {
            "passed": 0,
            "total": 0,
            "score": 0,
            "status": "No hidden testcases found for this problem",
            "details": []
        }

    passed = 0
    results = []

    for idx, tc in enumerate(tests):
        candidate_output = execute_code(req.language, req.code, tc["input"]).strip()
        expected_output = tc["expected"].strip()

        cand = " ".join(candidate_output.split())
        exp = " ".join(expected_output.split())

        ok = cand == exp

        if ok:
            passed += 1

        results.append({
            "case": idx + 1,
            "passed": ok,
            "expected": expected_output,
            "got": candidate_output
        })

    total = len(tests)
    score = int((passed / total) * 100)

    return {
        "passed": passed,
        "total": total,
        "score": score,
        "status": "Excellent" if score >= 80 else "Needs Improvement",
        "details": results
    }