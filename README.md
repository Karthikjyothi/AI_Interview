# 🤖 AI Interview System with Proctoring

An intelligent, end-to-end interview platform that simulates real-world technical and HR interviews using AI, with integrated **proctoring**, **resume-based questioning**, and **real-time evaluation**.

---

## 🚀 Live Features

### 🎤 AI Interview Engine

* HR + Technical interview modes
* Dynamic question generation using LLMs
* Adaptive difficulty based on candidate performance

### 📄 Resume-Based Questioning

* Upload resume
* Extract skills automatically
* Generate **personalized technical questions**

### 🧠 Intelligent Evaluation

* Answer analysis with feedback
* Score out of 10 for each response
* Continuous performance tracking

### 🛡️ AI Proctoring System

* 🎥 Face monitoring (MediaPipe)
* 👀 Detect looking away / phone usage
* 👥 Detect multiple faces
* ❌ Detect tab switching
* 🖥️ Screen sharing monitoring
* 📊 Real-time cheating score

### 💬 Modern UI (React)

* ChatGPT-style conversation interface
* Dark mode UI 🌙
* Smooth animations ✨
* Live timer ⏱️
* Progress tracking 📊

---

## 🏗️ Tech Stack

### Frontend

* React.js
* Framer Motion (animations)
* MediaPipe (face detection)
* WebSockets

### Backend

* FastAPI
* Python
* LiteLLM (LLM integration)

### AI / ML

* Resume parsing using LLM
* NLP-based feedback generation
* Face tracking & behavior analysis

---

## 📂 Project Structure

```
AI-Interview-System/
│
├── frontend/        # React UI
├── backend/         # FastAPI server
├── utils/           # AI + processing modules
├── outputs/         # Saved interview data
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/YOUR_USERNAME/AI-Interview-System.git
cd AI-Interview-System
```

---

### 2️⃣ Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

---

### 3️⃣ Add Environment Variables

Create `.env` file:

```
LLM_MODEL=your_model
GROQ_API_KEY=your_key
SPEECHMATICS_API_KEY=your_key
```

---

### 4️⃣ Run Backend

```
python -m uvicorn main:app --reload
```

---

### 5️⃣ Frontend Setup

```
cd frontend
npm install
npm start
```

---

## 🎯 How It Works

1. Upload resume
2. Select interview mode (HR / Technical)
3. Start interview
4. Answer questions in chat UI
5. AI evaluates responses
6. Proctoring monitors behavior
7. Get feedback + score

---

## 📊 Proctoring Score System

| Behavior             | Score Impact |
| -------------------- | ------------ |
| Tab switching        | +2           |
| Looking away         | +1           |
| Multiple faces       | +3           |
| No face detected     | +2           |
| Screen share stopped | +5           |

---

## 💡 Key Highlights

* Real-time AI interview simulation
* Resume-aware question generation
* Adaptive difficulty system
* Advanced proctoring features
* Clean and modern UI
* Full-stack AI integration

---

## 🚀 Future Improvements

* Coding interview with live compiler
* PDF resume parsing
* Proctoring report generation
* Interview history dashboard
* Deployment (AWS / Vercel)

---

## 👨‍💻 Author

**Karthik Jyothi**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub — it helps a lot!
