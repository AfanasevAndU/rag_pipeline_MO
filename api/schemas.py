from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5


class ChunkResponse(BaseModel):
    text: str
    lecture: str
    source: str
    chunk_id: int


class QuestionResponse(BaseModel):
    question: str
    chunks: List[ChunkResponse]