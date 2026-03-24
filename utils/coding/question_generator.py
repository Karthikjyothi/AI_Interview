from utils.llm_call import get_response_from_llm, parse_json_response
from utils.prompts import coding_question_generation

def generate_coding_question(job_description, resume_highlights):
    prompt = coding_question_generation.format(
        job_description=job_description,
        resume_highlights=resume_highlights
    )

    response = get_response_from_llm(prompt)
    return parse_json_response(response)