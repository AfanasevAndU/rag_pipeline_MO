# rag/chunker.py
import re
import nltk
from nltk.tokenize import sent_tokenize

# попытка убедиться, что требуемые ресурсы есть (не блокирует работу — скачает если нужно)
def ensure_nltk_resource(name):
    try:
        nltk.data.find(name)
    except LookupError:
        # скачиваем по короткому имени ('punkt' или 'punkt_tab')
        try:
            nltk.download(name.split("/")[-1])
        except Exception:
            # в некоторых окружениях загрузка может не пройти — тогда будем использовать fallback
            return False
    return True

# проверим оба варианта (чтобы покрыть разные версии NLTK)
_have_punkt = ensure_nltk_resource("tokenizers/punkt")
_have_punkt_tab = ensure_nltk_resource("tokenizers/punkt_tab")

def _simple_sent_tokenize(text: str):
    """
    Лёгкий резервный токенайзер, не требующий nltk.
    Делит текст по точке/вопрос/восклицанию + пробел(ы).
    """
    if not text:
        return []
    # оставляем знаки препинания в конце предложений, убираем лишние пробелы
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # фильтруем пустые результаты и короткие «шумные» фрагменты
    return [s.strip() for s in sentences if s.strip()]

def chunk_text(text, chunk_size=5, overlap=2):
    """
    Разбивает текст на чанки по предложениям.
    """
    # сначала пробуем nltk.sent_tokenize если ресурсы есть
    try:
        if _have_punkt or _have_punkt_tab:
            sentences = sent_tokenize(text)
        else:
            # если ресурсы не доступны, используем fallback
            sentences = _simple_sent_tokenize(text)
    except LookupError:
        # на всякий случай — если что-то пошло не так внутри sent_tokenize
        sentences = _simple_sent_tokenize(text)

    chunks = []
    step = max(1, chunk_size - overlap)

    for i in range(0, len(sentences), step):
        chunk = " ".join(sentences[i:i + chunk_size]).strip()
        if len(chunk) > 50:
            chunks.append(chunk)

    return chunks