import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from pydantic import BaseModel
from utils.analyze_candidate import analyze_candidate_response_and_generate_new_question
from utils.basic_details import get_ai_greeting_message

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
from utils.technical.question_generator import generate_technical_question
from utils.technical.evaluator import evaluate_technical_answer

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import WebSocket

cheating_scores = {}

@app.websocket("/ws/{candidate_id}")
async def websocket_endpoint(websocket: WebSocket, candidate_id: str):
    await websocket.accept()

    cheating_scores[candidate_id] = 0

    while True:
        data = await websocket.receive_json()

        event = data.get("event")

        if event == "TAB_SWITCH":
            cheating_scores[candidate_id] += 2

        elif event == "SCREEN_STOP":
            cheating_scores[candidate_id] += 5

        elif event == "LOOK_AWAY":
            cheating_scores[candidate_id] += 1

        elif event == "MULTIPLE_FACES":
            cheating_scores[candidate_id] += 3

        elif event == "NO_FACE":
            cheating_scores[candidate_id] += 2
            
        await websocket.send_json({
            "cheating_score": cheating_scores[candidate_id]
        })

# Request model
class InterviewRequest(BaseModel):
    question: str
    answer: str
    job_description: str
    resume_highlights: str
    mode: str   # NEW


@app.get("/")
def home():
    return {"message": "Backend running"}


# Start interview (greeting)
@app.post("/start")
def start_interview(name: str):
    greeting = get_ai_greeting_message(name)
    return {"question": greeting}


# Next question + feedback
@app.post("/next-question")
async def next_question(data: InterviewRequest):

    if data.mode == "technical":

        feedback = await evaluate_technical_answer(
            data.question,
            data.answer
        )

        next_q = generate_technical_question(
            data.job_description,
            data.resume_highlights
        )

        return {
            "next_question": next_q,
            "feedback": feedback
        }

    else:
        # HR mode
        next_q, feedback = await analyze_candidate_response_and_generate_new_question(
            data.question,
            data.answer,
            data.job_description,
            data.resume_highlights
        )

        return {
            "next_question": next_q,
            "feedback": feedback
        }