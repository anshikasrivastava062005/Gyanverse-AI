import os

DATA_FILE = "data/notes.txt"


def save_notes(text):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def get_context(query):
    if not os.path.exists(DATA_FILE):
        return ""

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = f.readlines()

    query_words = query.lower().split()

    scored_lines = []

    for line in data:
        score = sum(1 for word in query_words if word in line.lower())
        if score > 0:
            scored_lines.append((score, line))

    #  sort by relevance
    scored_lines.sort(reverse=True, key=lambda x: x[0])

    top_lines = [line for _, line in scored_lines[:5]]

    return " ".join(top_lines)