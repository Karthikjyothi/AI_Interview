from utils.llm_call import get_response_from_llm

# 🔥 REFINED PROMPT FOR DEEP-DIVE ANALYSIS
technical_prompt = """
You are an expert Technical Interviewer from a Top Tier Tech Company.
Your goal is to verify if the candidate actually built what is on their resume.

TASK:
Generate exactly ONE challenging technical question based on the Resume provided.

CONSTRAINTS:
1. Identify a specific Project or Skill from the Resume.
2. Ask a "Level 2" question (e.g., 'Why did you choose X over Y?', 'How did you handle the scale/bottleneck in Z?', 'Explain the data flow in project A').
3. DO NOT ask "What is X?" or "Tell me about Y."
4. If a project is mentioned, ask about a specific technical trade-off or a difficult bug.

RESUME HIGHLIGHTS:
{resume_highlights}

INSTRUCTIONS: 
Return ONLY the question text. No introductory text, no "Here is your question," no quotes.
"""

def generate_technical_question(job_description, resume_highlights):
    # Ensure we don't pass an empty string
    highlights = resume_highlights if resume_highlights.strip() else "The candidate is a Software Engineering student."
    
    prompt = technical_prompt.format(
        resume_highlights=highlights
    )

    try:
        response = get_response_from_llm(prompt)
        
        # 🧼 CLEANUP: Remove any AI filler text
        clean_question = response.replace("Question:", "").replace('"', "").strip()
        
        return clean_question
    except Exception as e:
        print(f"LLM Error in Generator: {e}")
        return "Can you explain the most technically challenging part of your main project?"