from pydantic import BaseModel
from typing import List

class QA(BaseModel):
    question: str
    answer: str

class Session(BaseModel):
    session_id: str
    qa_pairs: List[QA] = []
    is_complete: bool = False