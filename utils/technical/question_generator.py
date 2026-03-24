from utils.llm_call import get_response_from_llm

def generate_technical_question(job_description, resume_highlights, level="easy"):

    prompt = f"""
You are a technical interviewer.

Generate a technical interview question STRICTLY based on candidate skills.

Candidate Skills:
{resume_highlights}

Job Role:
{job_description}

Rules:
- Ask DSA / coding / core CS questions
- DO NOT ask system design questions
- DO NOT ask vague questions
- Focus on skills mentioned in resume
- Difficulty: {level}

Examples:
- If Python → ask coding or logic
- If DB → ask SQL
- If ML → ask ML basics

Return ONLY the question.
"""

    return get_response_from_llm(prompt)