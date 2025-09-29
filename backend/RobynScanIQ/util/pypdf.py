import PyPDF2


def extract_pdf_text(file_path: str) -> str:
    """Extrai todo o texto de um arquivo PDF."""
    text = ''
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ''
    return text
