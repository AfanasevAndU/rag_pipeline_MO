# api/reranker.py
from sentence_transformers import CrossEncoder

class RERRanker:
    """
    Reranker: пересортировка chunks по релевантности вопросу
    """
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        # Легкий cross-encoder, хорошо подходит для reranking
        self.model = CrossEncoder(model_name)

    def rerank(self, query, chunks):
        """
        query: str
        chunks: список payloads, у которых есть ключ 'text'
        """
        if not chunks:
            return []

        texts = [chunk["text"] for chunk in chunks]
        # вычисляем score для каждого chunk
        scores = self.model.predict([(query, text) for text in texts])

        # добавляем score в payload
        for i, chunk in enumerate(chunks):
            chunk["score"] = float(scores[i])

        # сортируем по убыванию score
        chunks = sorted(chunks, key=lambda x: x["score"], reverse=True)

        return chunks