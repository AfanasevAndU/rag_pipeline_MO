from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class VectorStore:

    def __init__(self):

        self.collection = "lectures"

        self.client = QdrantClient(path="./vector_db")

        self._create_collection()

    def _create_collection(self):

        collections = self.client.get_collections().collections

        names = [c.name for c in collections]

        if self.collection not in names:

            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=768,
                    distance=Distance.COSINE
                )
            )

    def add(self, vectors, payloads):

        points = []

        for i, vector in enumerate(vectors):

            points.append(
                PointStruct(
                    id=i,
                    vector=vector,
                    payload=payloads[i]
                )
            )

        self.client.upsert(
            collection_name=self.collection,
            points=points
        )