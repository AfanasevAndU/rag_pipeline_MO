import os

from rag.pdf_parser import extract_text_from_pdf
from rag.text_cleaner import clean_text
from rag.chunker import chunk_text
from rag.embeddings import embed
from rag.vector_store import VectorStore


DATA_PATH = "./data/lectures"


def ingest():

    store = VectorStore()

    texts = []
    payloads = []

    for file in os.listdir(DATA_PATH):

        if not file.endswith(".pdf"):
            continue

        path = os.path.join(DATA_PATH, file)

        lecture_name = file.replace(".pdf", "")

        # извлекаем текст
        raw = extract_text_from_pdf(path)

        # очищаем
        clean = clean_text(raw)

        # делаем chunks
        chunks = chunk_text(clean)

        for i, chunk in enumerate(chunks):

            texts.append(chunk)

            payloads.append({
                "text": chunk,
                "lecture": lecture_name,
                "source": file,
                "chunk_id": i
            })

    # создаём embeddings
    vectors = embed(texts)

    # загружаем в Qdrant
    store.add(vectors, payloads)


if __name__ == "__main__":
    ingest()