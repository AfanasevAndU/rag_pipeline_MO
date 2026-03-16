from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient


class RAGService:

    def __init__(self):

        self.model = SentenceTransformer("intfloat/multilingual-e5-base")

        self.qdrant = QdrantClient(path="./vector_db")

        self.collection = "lectures"

    def search(self, question, top_k=5):

        vector = self.model.encode(question, normalize_embeddings=True).tolist()

        result = self.qdrant.query_points(
            collection_name=self.collection,
            query=vector,
            limit=top_k
        )

        return [point.payload for point in result.points]