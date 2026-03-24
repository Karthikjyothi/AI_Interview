CODING_PROBLEMS = [
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "easy",
        "problem": """
Given an array of integers and a target, return indices of the two numbers such that they add up to target.

Input:
nums = [2,7,11,15], target = 9

Output:
[0,1]
""",
        "visible_tests": [
            {"input": "[2,7,11,15]\n9", "output": "[0,1]"}
        ],
        "hidden_tests": [
            {"input": "[3,2,4]\n6", "output": "[1,2]"},
            {"input": "[3,3]\n6", "output": "[0,1]"}
        ],
        "topics": ["arrays", "hashmap"]
    }
]
def get_problem_by_difficulty(level="easy"):
    for problem in CODING_PROBLEMS:
        if problem["difficulty"] == level:
            return problem
    return CODING_PROBLEMS[0]