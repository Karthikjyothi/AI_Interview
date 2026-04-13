import sys
import os

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

# ================= HOME =================
@app.get("/")
def home():
    return {"message": "Backend running"}

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

import requests

# 🚀 PISTON API (100% Free - No API Key Required)
PISTON_URL = "https://emkc.org/api/v2/piston/execute"

# Mapping frontend language names to Piston's expected names
LANG_MAP = {
    "python": "python",
    "java": "java",
    "cpp": "cpp",
    "javascript": "javascript"
}

@app.post("/run-code")
async def run_user_code(data: dict):
    lang = data.get('language', 'python')
    code = data.get('code', "")
    
    # Piston specific versions
    versions = {"python": "3.10.0", "java": "15.0.2", "cpp": "10.2.0", "javascript": "18.15.0"}
    
    payload = {
        "language": lang,
        "version": versions.get(lang, "3.10.0"),
        "files": [{"content": code}],
        "stdin": ""
    }

    try:
        response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)
        output_data = response.json()
        # Return the combined output (stdout + stderr)
        return {"output": output_data.get("run", {}).get("output", "No output from compiler.")}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}

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
        {text_content[:4000]}
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
        if not isinstance(result, dict) or "score" not in result:
            result = {
                "score": 50,
                "breakdown": {"role_match": 40, "impact_metrics": 30, "skill_depth": 50, "formatting": 80},
                "skills": [],
                "tips": [{"type": "bad", "msg": "AI failed to analyze. Please try again."}],
                "recommendations": []
            }

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
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_groq_llm(prompt):
    try:
        # Using llama-3.3-70b or mixtral-8x7b for high-quality analysis
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant that outputs only valid JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"} # Ensures we get clean JSON back
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Groq AI Error: {e}")
        return {"error": "AI could not process the resume"}
    
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