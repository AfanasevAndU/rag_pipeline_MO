# rag/chunker.py
import re

def clean_repeated_words(text, max_repeat=2):
    """
    Убирает слова, которые повторяются подряд более max_repeat раз.
    """
    def repl(match):
        word = match.group(1)
        return " ".join([word] * max_repeat)
    
    pattern = r'\b(\w+)\b(?:\s+\1\b){' + str(max_repeat) + r',}'
    return re.sub(pattern, repl, text, flags=re.IGNORECASE)

def chunk_text(text, chunk_size=90, overlap=30):
    """
    Делит текст на чанки по словам.
    chunk_size - количество слов в одном чанке
    overlap - количество слов для перекрытия
    """
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', " ", text).strip()
    
    words = text.split()
    chunks = []

    step = max(1, chunk_size - overlap)
    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        if len(chunk_words) > 5:
            chunk = " ".join(chunk_words)
            chunk = clean_repeated_words(chunk, max_repeat=2)
            chunks.append(chunk)

    return chunks