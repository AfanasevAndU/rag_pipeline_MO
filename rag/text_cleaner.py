import re


def clean_text(text):

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"(\b\w+\b)( \1\b)+", r"\1", text)

    return text.strip()