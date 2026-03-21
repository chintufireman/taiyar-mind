from typing import TypedDict, List
from llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END


class InterviewState(TypedDict):
    session_id: str
    conversation: list
    qna: list
    current_question: str


# 1. initialize - sets up the interview
def initialize(state: InterviewState) -> InterviewState:
    with open("prompts/interviewer.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    state["conversation"].append({"role": "system", "content": system_prompt})
    return state


# 2. ask_question - asks next question
def ask_question(state: InterviewState) -> InterviewState:
    response = get_llm().invoke(state["conversation"])
    state["conversation"].append({"role": "assistant", "content": response.content})
    state["current_question"] = response.content
    return state

# 3. receive_answer - processes user answer
def receive_answer(state: InterviewState, answer: str) -> InterviewState:
    state["conversation"].append({"role": "user", "content": answer})
    state["qna"].append({
        "question": state["current_question"],
        "answer": answer
    })
    return state
