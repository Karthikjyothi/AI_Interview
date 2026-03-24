from utils.llm_call import get_response_from_llm, parse_json_response


def evaluate_code_quality(problem, code):
    prompt = f"""
You are a senior software engineer.

Evaluate this solution.

Problem:
{problem["problem"]}

Code:
{code}

Return JSON:
{{
  "feedback": "",
  "time_complexity": "",
  "space_complexity": "",
  "improvements": ""
}}
"""

    response = get_response_from_llm(prompt)
    return parse_json_response(response)