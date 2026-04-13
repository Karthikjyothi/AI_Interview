from resume_analyzer.pyreparser.resume_parser import ResumeParser
from resume_analyzer.Courses import ds_course, web_course, android_course


def calculate_score(skills, text):
    score = 0

    # skill weight
    score += len(skills) * 5

    # bonus for important skills
    important = ["Python", "React", "SQL", "AI", "Machine learning"]

    for s in skills:
        if s in important:
            score += 5

    # section bonus
    if "project" in text:
        score += 15
    if "education" in text:
        score += 10
    if "experience" in text:
        score += 10

    return min(score, 100)


def generate_tips(text, skills):
    tips = []

    text = text.lower()

    # ✅ GOOD SECTIONS
    if "objective" in text or "summary" in text:
        tips.append({"type": "good", "msg": "You have added Objective/Summary"})
    else:
        tips.append({"type": "bad", "msg": "Add Objective/Summary"})

    if "education" in text:
        tips.append({"type": "good", "msg": "You have added Education Details"})
    else:
        tips.append({"type": "bad", "msg": "Add Education Details"})

    if "experience" in text:
        tips.append({"type": "good", "msg": "You have added Experience"})
    else:
        tips.append({"type": "bad", "msg": "Add Experience"})

    if "project" in text:
        tips.append({"type": "good", "msg": "You have added Projects"})
    else:
        tips.append({"type": "bad", "msg": "Add Projects"})

    if skills:
        tips.append({"type": "good", "msg": "You have added Skills"})
    else:
        tips.append({"type": "bad", "msg": "Add Skills section"})

    # ❌ MISSING SECTIONS
    if "hobbies" not in text:
        tips.append({"type": "bad", "msg": "Add Hobbies"})

    if "interest" not in text:
        tips.append({"type": "bad", "msg": "Add Interests"})

    if "achievement" not in text:
        tips.append({"type": "bad", "msg": "Add Achievements"})

    if "certification" not in text:
        tips.append({"type": "bad", "msg": "Add Certifications"})

    return tips


def analyze_resume_data(file_path):
    parser = ResumeParser(file_path)
    data = parser.get_extracted_data()

    if not data:
        return {"error": "Parsing failed"}

    skills = data.get("skills", [])
    text = parser._ResumeParser__text.lower()  # 🔥 get raw text

    # 🔥 DOMAIN DETECTION
    domain = "General"
    recommendations = []

    if any(skill in ["Python", "ML", "AI"] for skill in skills):
        domain = "Data Science"
        recommendations = ds_course

    elif any(skill in ["HTML", "CSS", "React"] for skill in skills):
        domain = "Web Development"
        recommendations = web_course

    elif any(skill in ["Android", "Kotlin"] for skill in skills):
        domain = "Android"
        recommendations = android_course

    # 🔥 NEW FEATURES
    tips = generate_tips(text, skills)
    score = calculate_score(skills, text)

    return {
        "name": data.get("name"),
        "email": data.get("email"),
        "skills": skills,
        "degree": data.get("degree"),
        "pages": data.get("no_of_pages"),
        "domain": domain,
        "score": score,
        "tips": tips,
        "strength": "Good" if len(skills) > 5 else "Average",
        "recommendations": recommendations
    }