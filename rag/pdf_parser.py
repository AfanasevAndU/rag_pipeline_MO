import pdfplumber


def extract_text_from_pdf(path: str) -> str:
    text = ""

    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text