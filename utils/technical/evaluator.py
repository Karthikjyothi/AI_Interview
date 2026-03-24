async def evaluate_technical_answer(question, answer):
    prompt = f"""
    Evaluate the candidate's technical answer.

    Question:
    {question}

    Answer:
    {answer}

    Give:
    1. Score out of 10
    2. Concept clarity
    3. Depth of understanding
    4. Real-world thinking
    5. Feedback

    Return JSON:
    {{
        "score": int,
        "feedback": "string"
    }}
    """

    return prompt