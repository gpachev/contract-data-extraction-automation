from typing import Optional
from docx import Document

def extract_docx_text(file_path: str) -> Optional[str]:
    """
    Extracts all text from a DOCX file.
    Args:
        file_path (str): Path to the DOCX file.
    Returns:
        Optional[str]: The extracted text, or None if extraction fails.
    """
    try:
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        # Optionally log the error here
        return None 