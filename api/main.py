from fastapi import FastAPI
from pydantic import BaseModel

from api.rag_service import RAGService

app = FastAPI()

rag = RAGService()


class SearchRequest(BaseModel):

    question: str
    top_k: int = 5


@app.get("/")
def root():

    return {"status": "RAG API running"}


@app.post("/search")
def search(request: SearchRequest):

    chunks = rag.search(request.question, request.top_k)

    return {
        "question": request.question,
        "chunks": chunks
    }