import re
import docx2txt
from pdfminer.high_level import extract_text as pdf_extract_text

# 📄 Extract text
def extract_text(file_path, ext):
    try:
        if ext == ".pdf":
            return pdf_extract_text(file_path)
        elif ext == ".docx":
            return docx2txt.process(file_path)
    except:
        return ""

# 📧 Email
def extract_email(text):
    match = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
    return match[0] if match else None

# 📱 Phone
def extract_mobile_number(text, custom_regex=None):
    match = re.findall(r'\+?\d[\d -]{8,12}\d', text)
    return match[0] if match else None

# 🧠 Skills (IMPORTANT FIX)
def extract_skills(nlp_text, noun_chunks, skills_file=None):
    SKILLS_DB = [
        "python", "java", "c++", "react", "node", "sql",
        "machine learning", "ai", "deep learning",
        "html", "css", "javascript", "flask", "django",
        "aws", "docker", "kubernetes", "mongodb"
    ]

    text = nlp_text.text.lower()
    skills = []

    for skill in SKILLS_DB:
        if skill in text:
            skills.append(skill.capitalize())

    return list(set(skills))

# 👤 Name
import re

def extract_name(nlp_text, matcher=None):

    text = nlp_text.text.strip()

    # 🔥 STEP 1 — NLP-based extraction (but filtered)
    for ent in nlp_text.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()

            # ❌ reject bad names
            bad_words = ["harry", "potter", "react", "node", "express", "project"]
            if any(word in name.lower() for word in bad_words):
                continue

            # accept only clean names
            if 2 <= len(name.split()) <= 4:
                return name

    # 🔥 STEP 2 — First words fallback
    words = text.split()[:10]

    candidate = " ".join(words)
    candidate = re.sub(r'[^A-Za-z ]', '', candidate)

    parts = candidate.split()

    if len(parts) >= 2:
        return " ".join(parts[:3])

    # 🔥 STEP 3 — Email fallback (very reliable)
    email = extract_email(text)
    if email:
        name_part = email.split("@")[0]
        name_part = name_part.replace(".", " ").replace("_", " ")
        return name_part.title()

    return "Not Found"

def extract_entities_wih_custom_model(doc):
    return {}

def extract_entity_sections_grad(text):
    return {}

def get_number_of_pages(file):
    return 1