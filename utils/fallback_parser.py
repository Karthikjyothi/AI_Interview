import re

def extract_name_fallback(resume_text):
    lines = resume_text.strip().split("\n")
    for line in lines[:5]:
        if len(line.split()) >= 2 and len(line) < 40:
            return line.strip()
    return "Unknown"


def extract_skills_fallback(resume_text):
    skills_keywords = [
        "Python", "Java", "C++", "Machine Learning", "AI",
        "SQL", "Deep Learning", "React", "Node", "AWS"
    ]

    found = []
    for skill in skills_keywords:
        if skill.lower() in resume_text.lower():
            found.append(skill)

    return found