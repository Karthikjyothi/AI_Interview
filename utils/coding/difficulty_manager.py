def next_difficulty(current):
    order = ["easy", "medium", "hard"]

    if current not in order:
        return "easy"

    idx = order.index(current)
    if idx + 1 < len(order):
        return order[idx + 1]

    return "hard"