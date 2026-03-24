import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
from utils.coding.question_bank import get_problem_by_difficulty
from utils.coding.evaluator import evaluate_problem
from utils.coding.scoring import calculate_score
from utils.coding.difficulty_manager import next_difficulty
from utils.coding.llm_feedback import evaluate_code_quality
from utils.coding.question_generator import generate_coding_question
from utils.technical.question_generator import generate_technical_question
from utils.technical.evaluator import evaluate_technical_answer
from utils.proctoring.gaze_monitor import start_gaze_monitor
from utils.proctoring.advanced_monitor import start_advanced_proctoring
from utils.proctoring.screen_monitor import start_screen_monitor
import asyncio
import os
import time
from datetime import datetime
from utils.proctoring.tab_monitor import enforce_fullscreen
from utils.proctoring.camera_monitor import start_camera_monitor
from utils.proctoring.fullscreen import start_fullscreen
from utils.proctoring.gaze_monitor import start_gaze_monitor
from utils import (
    transcribe_with_speechmatics,
    extract_resume_info_using_llm,
    get_ai_greeting_message,
    get_final_thanks_message,
    speak_text,
    analyze_candidate_response_and_generate_new_question,
    get_feedback_of_candidate_response,
    get_overall_evaluation_score,
    save_interview_data,
    load_content_streamlit,
)

TOTAL_CODING_QUESTIONS = 3
MAX_QUESTIONS = 15


# Configuration and Styling
def setup_page_config():
    """Setup page configuration and custom CSS"""
    st.set_page_config(page_title="AI Interview App", layout="wide")

    st.markdown(
        """
    <style>
    .audio-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
        border: 2px solid #e9ecef;
    }
    .interview-progress {
        background-color: #e8f5e8;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        "interview_started": False,
        "name": "",
        "resume_highlights": "",
        "job_description": "",
        "qa_index": 1,
        "conversations": [],
        "current_question": "",
        "question_spoken": False,
        "awaiting_response": False,
        "processing_audio": False,
        "messages": [],
        "interview_completed": False,
        "max_questions": MAX_QUESTIONS,
        "ai_voice": "Alex (Male)",
        "thanks_message_prepared": False,
        "thanks_message_spoken": False,
        "show_final_results": False,
    }
    if "cheating_score" not in st.session_state:
        st.session_state["cheating_score"] = 0
    if "coding_round" not in st.session_state:
        st.session_state["coding_round"] = 1

    if "coding_scores" not in st.session_state:
        st.session_state["coding_scores"] = []

    if "current_difficulty" not in st.session_state:
        st.session_state["current_difficulty"] = "easy"
    if "current_problem" not in st.session_state:
        st.session_state["current_problem"] = None
    if "tab_switch_count" not in st.session_state:
        st.session_state["tab_switch_count"] = 0
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_ai_voice_details():
    """Get AI voice configuration"""
    return {
        "Alex (Male)": {"name": "Alex", "code": "en-US-GuyNeural"},
        "Aria (Female)": {"name": "Aria", "code": "en-US-AriaNeural"},
        "Natasha (Female)": {"name": "Natasha", "code": "en-AU-NatashaNeural"},
        "Sonia (Female)": {"name": "Sonia", "code": "en-GB-SoniaNeural"},
    }


def get_instructions():
    """Get instructions for the user"""
    content = """
    #### Please follow these steps to use the AI Interview App:
    1. **Upload Resume**: Upload your resume in PDF format.
    2. **Job Description**: Paste the job description.
    3. **Start Interview**: Click the "Start Interview" button to begin the AI-driven interview.
    4. **Maximum Questions**: You can set the maximum number of questions for the interview. (default: 5)
    5. **Voice Selection**: Choose the AI voice for the interview.(default: Alex (Male))
    6. **Answer Questions**: Answer the questions posed by the AI interviewer.
    7. **Review Results**: After the interview, review your performance and feedback.

    **Note**: The AI interviewer will ask you questions based on your resume and the job description.

    I hope you find the experience helpful!
    """
    return st.markdown(content)


def render_sidebar():
    """Render sidebar with candidate information and settings"""
    st.sidebar.title("Candidate Information")

    # File upload
    uploaded_resume = st.sidebar.file_uploader("Upload your Resume (PDF)", type=["pdf"])

    # Job description
    job_description = st.sidebar.text_area("Paste the Job Description")

    # Settings
    max_questions = st.sidebar.number_input(
        "Maximum number of questions",
        min_value=1,
        max_value=20,
        value=MAX_QUESTIONS,
    )
    st.session_state["max_questions"] = max_questions

    ai_voice = st.sidebar.radio(
        "Select AI Interviewer Voice",
        ["Alex (Male)", "Aria (Female)", "Natasha (Female)", "Sonia (Female)"],
    )
    st.session_state["ai_voice"] = ai_voice

    submit = st.sidebar.button("Submit")

    return uploaded_resume, job_description, submit


def process_resume_submission(uploaded_resume, job_description):
    """Process resume and job description submission"""
    with st.spinner("Processing resume..."):
        resume_content = load_content_streamlit(uploaded_resume)
        name, resume_highlights = extract_resume_info_using_llm(resume_content)

    # Store in session state
    st.session_state["name"] = name
    st.session_state["resume_highlights"] = resume_highlights
    st.session_state["job_description"] = job_description

    # Reset interview state
    reset_interview_state()

    st.success(f"Candidate Name: {name}")


def reset_interview_state():
    """Reset interview-related session state"""
    interview_keys = [
        "interview_started",
        "qa_index",
        "conversations",
        "current_question",
        "question_spoken",
        "awaiting_response",
        "processing_audio",
        "messages",
        "interview_completed",
        "thanks_message_prepared",
        "thanks_message_spoken",
        "show_final_results",
    ]

    for key in interview_keys:
        if key == "interview_started" or key == "interview_completed":
            st.session_state[key] = False
        elif key in ["qa_index"]:
            st.session_state[key] = 1
        elif key in ["conversations", "messages"]:
            st.session_state[key] = []
        elif key in ["current_question"]:
            st.session_state[key] = ""
        else:
            st.session_state[key] = False


def start_interview():
    """Initialize and start the interview"""
    st.session_state["interview_started"] = True
    reset_interview_state()
    st.session_state["interview_started"] = True  # Reset above sets this to False

    # Get greeting message
    ai_voice_details = get_ai_voice_details()
    interviewer_name = ai_voice_details[st.session_state["ai_voice"]]["name"]
    greeting_message = get_ai_greeting_message(
        st.session_state["name"], interviewer_name=interviewer_name
    )

    st.session_state["current_question"] = greeting_message
    st.session_state["messages"].append(
        {"role": "assistant", "content": greeting_message}
    )


def display_chat_messages():
    """Display all chat messages from history"""
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def speak_current_question():
    """Speak the current question if not already spoken"""
    if st.session_state["current_question"] and not st.session_state["question_spoken"]:
        with st.spinner("AI Interviewer is speaking..."):
            ai_voice_details = get_ai_voice_details()
            speak_text(
                st.session_state["current_question"],
                voice=ai_voice_details[st.session_state["ai_voice"]]["code"],
            )
        st.session_state["question_spoken"] = True
        st.session_state["awaiting_response"] = True
        st.rerun()


def generate_next_question():
    """Generate and prepare the next question"""
    if st.session_state["conversations"]:
        last_conv = st.session_state["conversations"][-1]
        next_question, _ = asyncio.run(
            analyze_candidate_response_and_generate_new_question(
                last_conv["Question"],
                last_conv["Candidate Answer"],
                st.session_state["job_description"],
                st.session_state["resume_highlights"],
            )
        )
    else:
        next_question = "Tell me about yourself and your experience."

    st.session_state["current_question"] = next_question
    st.session_state["messages"].append({"role": "assistant", "content": next_question})
    st.session_state["question_spoken"] = False
    st.session_state["awaiting_response"] = False


def process_candidate_response(transcript):
    """Process candidate's response and move to next state"""
    # Add candidate's answer to chat
    st.session_state["messages"].append({"role": "user", "content": transcript})

    # Generate feedback for this response
    if st.session_state["qa_index"] < st.session_state["max_questions"] - 1:
        # Not the last question - generate next question and feedback
        next_question, feedback = asyncio.run(
            analyze_candidate_response_and_generate_new_question(
                st.session_state["current_question"],
                transcript,
                st.session_state["job_description"],
                st.session_state["resume_highlights"],
            )
        )
    else:
        # Last question - only generate feedback
        feedback = asyncio.run(
            get_feedback_of_candidate_response(
                st.session_state["current_question"],
                transcript,
                st.session_state["job_description"],
                st.session_state["resume_highlights"],
            )
        )

    # Store conversation
    st.session_state["conversations"].append(
        {
            "Question": st.session_state["current_question"],
            "Candidate Answer": transcript,
            "Evaluation": feedback["score"],
            "Feedback": feedback["feedback"],
        }
    )
    st.session_state["hr_score"] = feedback["score"]

    # Move to next question or complete interview
    st.session_state["qa_index"] += 1
    st.session_state["processing_audio"] = False
    st.session_state["awaiting_response"] = False

    if st.session_state["qa_index"] <= st.session_state["max_questions"]:
        # Prepare next question
        generate_next_question()
        st.success("✅ Answer recorded! Preparing next question...")
    else:
        # Interview completed - prepare thanks message
        st.session_state["interview_completed"] = True
        prepare_thanks_message()


def prepare_thanks_message():
    """Prepare and display thanks message"""
    if not st.session_state["thanks_message_prepared"]:
        final_note = get_final_thanks_message(st.session_state["name"])
        st.session_state["messages"].append(
            {"role": "assistant", "content": final_note}
        )
        st.session_state["thanks_message_prepared"] = True
        st.session_state["qa_index"] -= 1
        st.rerun()


def speak_thanks_message():
    """Speak the thanks message"""
    if (
        st.session_state["thanks_message_prepared"]
        and not st.session_state["thanks_message_spoken"]
    ):

        # Get the last message (thanks message)
        thanks_message = st.session_state["messages"][-1]["content"]

        with st.spinner("AI Interviewer is giving final remarks..."):
            ai_voice_details = get_ai_voice_details()
            speak_text(
                thanks_message,
                voice=ai_voice_details[st.session_state["ai_voice"]]["code"],
            )

        st.session_state["thanks_message_spoken"] = True
        st.success("🎉 Interview completed! Thank you for your time.")

        # Now show final results
        st.session_state["show_final_results"] = True
        st.rerun()

def init_state():
    keys = {
        "cheating_score": 0,
        "tab_switch_count": 0,
        "look_away_count": 0,
        "multiple_faces": 0
    }

    for k, v in keys.items():
        if k not in st.session_state:
            st.session_state[k] = v
            
def handle_audio_recording():
    """Handle audio recording and processing"""
    if not (
        st.session_state["awaiting_response"]
        and not st.session_state["processing_audio"]
    ):
        return

    st.write("**🎙️ Please record your answer to the question above**")

    audio_key = f"audio_input_{st.session_state['qa_index']}_{len(st.session_state['messages'])}"
    audio_data = st.audio_input("Record your answer", key=audio_key)

    if audio_data is not None:
        st.session_state["processing_audio"] = True

        with st.spinner("Processing your answer..."):
            # Save audio file
            name = st.session_state["name"]
            filename = f"audio/{name}/{name}_{st.session_state['qa_index'] + 1}.wav"
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, "wb") as f:
                f.write(audio_data.read())

            # Transcribe audio
            transcript = transcribe_with_speechmatics(filename)

            if transcript and transcript.strip():
                process_candidate_response(transcript)
                st.rerun()
            else:
                st.error("No speech detected in audio. Please try recording again.")
                st.session_state["processing_audio"] = False


def display_final_results():
    """Display final interview results"""
    if (
        not st.session_state["show_final_results"]
        or not st.session_state["conversations"]
    ):
        return

    with st.spinner("Calculating final score..."):
        final_score = get_overall_evaluation_score(st.session_state["conversations"])

        # Save interview data
        now = datetime.now().isoformat() + "Z"
        interview_data = {
            "name": st.session_state["name"],
            "createdAt": now,
            "updatedAt": now,
            "id": 1,
            "job_description": st.session_state["job_description"],
            "resume_highlights": st.session_state["resume_highlights"],
            "conversations": st.session_state["conversations"],
            "overall_score": round(final_score, 2),
        }
        save_interview_data(interview_data, candidate_name=st.session_state["name"])

    # Display results
    st.subheader("🎉 Interview Results")
    st.markdown(f"**Candidate:** {st.session_state['name']}")
    st.markdown(f"**Overall Score:** {final_score:.2f}/10")

    # Show detailed summary
    st.subheader("Detailed Interview Summary")
    for i, conv in enumerate(st.session_state["conversations"], 1):
        with st.expander(f"Question {i} (Score: {conv['Evaluation']}/10)"):
            st.write(f"**Q:** {conv['Question']}")
            st.write(f"**A:** {conv['Candidate Answer']}")
            st.write(f"**Feedback:** {conv['Feedback']}")

    # New interview option
    if st.button("Start New Interview"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def render_interview_progress():
    """Render interview progress indicator"""
    if st.session_state.get("interview_started", False):
        progress_text = f"Question {st.session_state['qa_index']} of {st.session_state['max_questions']}"
        st.markdown(
            f'<div class="interview-progress"><strong>{progress_text}</strong></div>',
            unsafe_allow_html=True,
        )


def main():
    """Main application function"""

    # Setup
    setup_page_config()
    initialize_session_state()

    # Initialize coding state
    if "coding_question" not in st.session_state:
        st.session_state["coding_question"] = None

    if "submitted_code" not in st.session_state:
        st.session_state["submitted_code"] = None

    # Header
    st.title("🤖 AI Interview System")

    # Tabs
    # tab1, tab2 = st.tabs(["HR Interview", "Coding Interview"])
    tab1, tab2, tab3 = st.tabs(
        ["HR Interview", "Technical Interview", "Coding Interview"]
    )

    # ================= HR INTERVIEW TAB ================= #
    with tab1:

        insturctions = st.empty()

        if not st.session_state["interview_started"]:
            insturctions = get_instructions()

        # Sidebar
        uploaded_resume, job_description, submit = render_sidebar()

        # Process submission
        if submit and uploaded_resume and job_description:
            insturctions.empty()
            process_resume_submission(uploaded_resume, job_description)

            # Save for coding round
            st.session_state["job_description"] = job_description

        # Start interview button
        if st.session_state["name"] and not st.session_state["interview_started"]:
            if st.button("Start Interview"):
                start_interview()
                st.rerun()

        # Interview section
        if st.session_state.get("interview_started", False):
            start_fullscreen()
            start_camera_monitor()
            start_gaze_monitor()
            render_interview_progress()
            '''enforce_fullscreen()'''
            start_advanced_proctoring()
            start_screen_monitor()

            # Show chat history
            st.subheader("Interview Chat")
            display_chat_messages()

            # Handle different interview states
            if not st.session_state["interview_completed"]:
                speak_current_question()
                handle_audio_recording()

            elif not st.session_state["thanks_message_prepared"]:
                prepare_thanks_message()

            elif not st.session_state["thanks_message_spoken"]:
                speak_thanks_message()

            else:
                display_final_results()

    # ================= TECHNICAL INTERVIEW TAB ================= #
    with tab2:

        st.header("🧠 Technical Interview")

        # Start technical interview
        if st.button("Start Technical Interview"):
            question = generate_technical_question(
                st.session_state.get("job_description", ""),
                st.session_state.get("resume_highlights", []),
            )
            st.session_state["technical_question"] = question
        
        st.markdown(f"### 🚨 Cheating Score: {st.session_state.get('cheating_score', 0)}")
        if st.checkbox("I did NOT stop screen sharing"):
            pass
        else:
            st.session_state["cheating_score"] = st.session_state.get("cheating_score", 0) + 5
        # Show question
        if st.session_state.get("technical_question"):

            st.subheader("Technical Question")
            st.write(st.session_state["technical_question"])

            # Voice or text answer
            answer = st.text_area("Write or speak your answer")

            if st.button("Submit Technical Answer"):

                if answer.strip() == "":
                    st.warning("Please answer before submitting.")
                else:
                    feedback = asyncio.run(
                        evaluate_technical_answer(
                            st.session_state["technical_question"], answer
                        )
                    )

                    score = feedback["score"]
                    st.write("DEBUG feedback:", feedback)

                    st.session_state["technical_score"].append(score)

                    st.write("Score:", score)
                    st.write("Feedback:", feedback["feedback"])

                    # Adaptive difficulty
                    if score > 7:
                        level = "hard"
                    elif score > 4:
                        level = "medium"
                    else:
                        level = "easy"

                    st.session_state["technical_question"] = (
                        generate_technical_question(
                            st.session_state.get("job_description", ""),
                            st.session_state.get("resume_highlights", []),
                            level=level,
                        )
                    )
    # ================= CODING INTERVIEW TAB ================= #

    with tab3:

        st.header("💻 Coding Interview")

        # ===== Check if coding round finished =====
        if st.session_state["coding_round"] > TOTAL_CODING_QUESTIONS:

            st.success("🎉 Coding Interview Completed!")

            # Final coding score
            final_score = sum(st.session_state["coding_scores"]) / len(
                st.session_state["coding_scores"]
            )

            st.subheader("💻 Final Coding Score")
            st.write(round(final_score, 2))

            # Detailed breakdown
            st.subheader("📊 Coding Performance Breakdown")
            for i, s in enumerate(st.session_state["coding_scores"]):
                st.write(f"Question {i+1}: {round(s, 2)}")

            # ===== Overall score (HR + Technical + Coding) =====
            hr_score = st.session_state.get("hr_score", None)

            technical_scores = st.session_state.get("technical_score", [])

            if technical_scores:
                technical_avg = sum(technical_scores) / len(technical_scores)
            else:
                technical_avg = 0

            if hr_score is not None:
                overall_score = (final_score + hr_score + technical_avg) / 3

                st.subheader("🏆 Overall Interview Score")
                st.write(round(overall_score, 2))

                # Show breakdown (optional but impressive)
                st.write("HR Score:", round(hr_score, 2))
                st.write("Technical Score:", round(technical_avg, 2))
                st.write("Coding Score:", round(final_score, 2))

            else:
                st.info("HR score not available yet.")

            # Restart button
            if st.button("Restart Coding Interview"):
                st.session_state["coding_round"] = 1
                st.session_state["coding_scores"] = []
                st.session_state["current_difficulty"] = "easy"
                st.session_state["current_problem"] = None
                st.rerun()

        # ===== Active coding round =====
        else:

            # Load problem
            if st.session_state.get("current_problem") is None:
                st.session_state["current_problem"] = get_problem_by_difficulty(
                    st.session_state["current_difficulty"]
                )

            problem = st.session_state["current_problem"]

            # Round info
            st.write(
                f"Question {st.session_state['coding_round']} of {TOTAL_CODING_QUESTIONS}"
            )
            st.write(f"Difficulty: {problem['difficulty']}")

            # Show problem
            st.subheader(problem["title"])
            st.write(problem["problem"])

            # Code editor
            code = st.text_area(
                "Write your Python solution",
                height=300,
                placeholder="Example:\n\nn = int(input())\nprint(n)",
            )

            # Submit
            if st.button("Run and Submit"):

                if code.strip() == "":
                    st.warning("Please write code before submitting.")

                else:
                    visible, hidden = evaluate_problem(code, problem)
                    score = calculate_score(visible, hidden)

                    st.write("Visible test results:", visible)
                    st.write("Score:", score)

                    feedback = evaluate_code_quality(problem, code)

                    if feedback:
                        st.subheader("AI Feedback")
                        st.write(feedback.get("feedback", ""))
                        st.write(
                            "Time Complexity:", feedback.get("time_complexity", "")
                        )
                        st.write(
                            "Space Complexity:", feedback.get("space_complexity", "")
                        )
                    # Save score
                    st.session_state["coding_scores"].append(score)

                    # Move difficulty
                    st.session_state["current_difficulty"] = next_difficulty(
                        problem["difficulty"]
                    )

                    # Next question
                    st.session_state["coding_round"] += 1
                    st.session_state["current_problem"] = None

                    st.rerun()


if __name__ == "__main__":
    main()
