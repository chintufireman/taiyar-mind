from typing import Annotated
from fastapi import APIRouter, Form, File,UploadFile
import uuid
from graph.interview_graph import InterviewState, initialize, ask_question, receive_answer
from llm import get_llm
from models import AnswerRequest
from services.services import load_voice_model

router = APIRouter()
sessions = {}


@router.post("/interview/start")
async def start_interview():
    session_id = str(uuid.uuid4())

    state: InterviewState = {
        "session_id": session_id,
        "conversation": [],
        "qna": [],
        "current_question": "",
    }

    state = initialize(state)       # adds system prompt
    state = ask_question(state)     # gets first question from LLM

    sessions[session_id] = state
    return {"session_id": session_id, "question": state["current_question"]}

@router.post("/interview/answer")
async def answer_interview(request: AnswerRequest):
    if request.session_id not in sessions:
        return {"error": "Session not found"}

    state = sessions[request.session_id]
    state = receive_answer(state, request.answer)   # stores answer
    state = ask_question(state)             # asks next question
    sessions[request.session_id] = state

    return {"session_id": request.session_id, "question": state["current_question"]}


@router.get("/interview/result")
async def interview_result(session_id: str):
    if session_id not in sessions:
        return {"error": "Session not found"}
    state = sessions[session_id]
    qna = state["qna"]

    # build evaluation prompt
    evaluation_prompt = "Evaluate this interview and give overall feedback:\n\n"
    for i, qa in enumerate(qna):
        evaluation_prompt += f"Q{i+1}: {qa['question']}\nAnswer: {qa['answer']}\n\n"
    evaluation_prompt += "Give total score out of 10, strengths and weaknesses."

    response = get_llm().invoke([{"role": "user", "content": evaluation_prompt}])
    return response

@router.post("/interview/voice")
async def interview_voice_response(session_id: Annotated[str, Form(...)],
                                   answer: Annotated[UploadFile, File(...)]):


    transcript = await load_voice_model(answer)
    state = sessions[session_id]
    state = receive_answer(state, transcript.text)
    state = ask_question(state)
    sessions[session_id] = state

    return {"session_id": session_id, "question": state["current_question"]}

