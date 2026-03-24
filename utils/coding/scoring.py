def calculate_score(visible, hidden):
    total = len(visible) + len(hidden)
    passed = sum(visible) + sum(hidden)

    score = (passed / total) * 100
    return score