# api/rag_service.py
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from api.reranker import RERRanker

class RAGService:

    def __init__(self):
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")
        self.qdrant = QdrantClient(path="./vector_db")
        self.collection = "lectures"
        self.reranker = RERRanker()

    def search(self, question, top_k=5, lecture_filter=None):
        """
        lecture_filter: str, если указано - искать только в этой лекции
        """
        vector = self.model.encode(question, normalize_embeddings=True).tolist()
        
        # фильтр по метаданным
        q_filter = {"must": [{"key": "lecture", "match": {"value": lecture_filter}}]} if lecture_filter else None

        result = self.qdrant.query_points(
            collection_name=self.collection,
            query=vector,
            limit=top_k * 5,
            query_filter=q_filter
        )

        chunks = [point.payload for point in result.points]
        chunks = self.reranker.rerank(question, chunks)
        return chunks[:top_k]