from utils.coding.test_case_engine import run_code


def evaluate_problem(user_code, problem):
    visible_results = []
    hidden_results = []

    # Visible tests
    for test in problem["visible_tests"]:
        output, err = run_code(user_code, test["input"])
        visible_results.append(output == test["output"])

    # Hidden tests
    for test in problem["hidden_tests"]:
        output, err = run_code(user_code, test["input"])
        hidden_results.append(output == test["output"])

    return visible_results, hidden_results