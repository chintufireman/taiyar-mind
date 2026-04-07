from pydantic import BaseModel
from typing import List, Annotated

class QA(BaseModel):
    question: str
    answer: str

class Session(BaseModel):
    session_id: str
    qa_pairs: List[QA] = []


class AnswerRequest(BaseModel):
    session_id: str
    answer: str
