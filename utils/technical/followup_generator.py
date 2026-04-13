from utils.llm_call import get_response_from_llm

def generate_followup_question(history, resume):

    try:
        last = history[-1] if history else {"question": "", "answer": ""}

        question = last.get("question", "")
        answer = last.get("answer", "")

        if not question or not answer:
            return "Can you explain your previous answer in more detail?"

        prompt = f"""
You are a senior technical interviewer.

Previous Question:
{question}

Candidate Answer:
{answer}

Ask a FOLLOW-UP question.

Rules:
- Go deeper into same topic
- Ask WHY / HOW / edge cases
- Challenge the candidate
- Do NOT change topic

Resume:
{resume}

Return only the question.
"""

        response = get_response_from_llm(prompt)

        return response or "Can you elaborate more on your answer?"

    except Exception as e:
        print("FOLLOWUP ERROR:", e)
        return "Can you explain your previous answer more clearly?"