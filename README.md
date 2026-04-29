# 🚀 AI Career Prep Platform – Resume Analyzer + AI Interview + TCS Mock Test + Proctoring

A complete AI-powered placement preparation ecosystem built for students and job aspirants.
This platform combines:

* 📄 Professional ATS Resume Analysis
* 🎤 AI Mock Interviews (HR + Technical + Resume Based)
* 📝 TCS Full Length Mock Assessment
* 💻 Live Coding Compiler & Hidden Testcase Evaluation
* 🛡️ Fullscreen Proctoring + Anti-Cheat Monitoring
* 📊 AI Performance Dashboards

into one unified placement readiness platform.

---

# 🌟 Major Features

---

## 📄 1. Professional ATS Resume Analyzer

Upload candidate resume PDF and get:

* ATS Match Percentage
* Role Match Score
* Impact / STAR Evaluation
* Skill Depth Analysis
* Formatting Analysis
* Detected Technical Skills
* Missing ATS Keywords
* Detailed AI Critique
* Personalized Recommended Courses
* Candidate Level Prediction
* Best Suited Job Domain

---

## 🎤 2. AI Mock Interview Engine

Supports:

* HR Interview Mode
* Technical Interview Mode
* Resume-Based Personalized Interview

Capabilities:

* AI asks dynamic follow-up questions
* Questions adapt based on user answers
* Real-time AI scoring
* Final interview feedback dashboard

---

## 💻 3. TCS Full Mock Assessment

Complete placement style test with:

* Numerical Ability
* Verbal Ability
* Logical Reasoning
* Advanced Quant & Reasoning
* Coding Round

Features:

* Section wise timer
* Final Submit Test workflow
* Fullscreen exam lock
* Auto submit after 3 fullscreen violations
* AI generated final dashboard
* Section wise performance analytics

---

## 🧪 4. Coding Compiler + Hidden Testcase Judge

Supports multiple languages:

* Python
* Java
* C
* C++
* JavaScript

Candidate can:

* Write code in Monaco Editor
* Run code with custom input
* Submit code for hidden testcase evaluation
* View pass/fail verdict and coding score

---

## 🛡️ 5. AI Proctoring & Anti-Cheat

Integrated anti-cheating systems:

* Fullscreen enforcement
* Fullscreen exit violation tracking
* Auto submit on 3 violations
* MediaPipe face monitoring
* Tab switching detection
* Candidate behavior monitoring during interviews

---

## 📊 6. AI Performance Dashboards

Platform generates:

* Resume ATS Dashboard
* Interview Feedback Dashboard
* TCS Mock Performance Dashboard
* AI Generated Strength/Weakness Analysis

---

# 🛠️ Tech Stack

## Frontend

* React.js
* Framer Motion
* Monaco Editor
* MediaPipe
* WebSockets

## Backend

* FastAPI
* Python
* SQLite3
* Groq LLM API
* Multi-language compiler execution

## AI Layer

* Groq LLM (`llama-3.1-8b-instant`)
* Dynamic JSON prompt engineering
* Resume ATS reasoning
* Mock question generation
* AI performance feedback

---

# 📂 Complete Project Structure

```bash
AI-Interview-System/
│
├── backend/
│   ├── main.py
│   ├── coding_testcases.py
│   ├── interview.db
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env
│
└── README.md
```

---

# ⚙️ FULL SETUP GUIDE (NEW LAPTOP / FRESH CLONE)

---

## 1. Clone Repository

```bash
git clone https://github.com/Karthikjyothi/medical-ai-system.git
cd medical-ai-system
```

---

## 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Backend Environment Variables

Create `backend/.env`

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 4. Required Local Compilers Installation

Install these on system PATH:

### Python

```bash
python --version
```

### GCC / G++

```bash
gcc --version
g++ --version
```

### Java

```bash
javac -version
```

### Node

```bash
node -v
```

These are required for coding round execution.

---

## 5. Run Backend Server

```bash
uvicorn main:app --reload
```

Backend runs on:

```bash
http://localhost:8000
```

---

## 6. Frontend Setup

Open new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

```bash
http://localhost:3000
```

---

# ▶️ COMPLETE PROJECT RUN ORDER (VERY IMPORTANT)

Always run in this order:

### Terminal 1:

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

### Terminal 2:

```bash
cd frontend
npm start
```

Then open browser:

```bash
http://localhost:3000
```

---

# 🎯 MODULES AVAILABLE INSIDE APP

* Resume Analyzer
* Practice Interview
* TCS Mock Test
* Coding Round
* AI Proctoring

---

# 🧠 DATABASE FILES USED

Main project uses:

```bash
backend/interview.db
```

Contains:

* mock_questions
* results
* interview records

Do not delete this DB.

---

# 🔐 Important Notes Before Running

### If coding round shows compiler errors:

verify system compilers are installed and available in terminal.

### If resume AI fails:

verify `GROQ_API_KEY` inside `.env`

### If frontend package missing:

run:

```bash
npm install
```

---

# ☁️ GitHub Update Commands (SAVE CURRENT WORK)

Whenever local changes are done:

```bash
git add .
git add -f backend/.env
git add -f backend/*.db
git commit -m "latest full project update"
git push origin main --force
```

---

# 💡 Current Premium Capabilities

* Dynamic ATS AI Resume Analysis
* Dynamic AI Mock Interviews
* Dynamic TCS Paper Generation
* Hidden Testcase Coding Judge
* Fullscreen Auto Submit Proctoring
* AI Final Feedback

---

# 👨‍💻 Developed By

**Karthik Jyothi**

AI Career Preparation Platform

---

# ⭐ GitHub Support

If this project helps you, give the repository a ⭐
