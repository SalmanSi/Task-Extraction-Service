import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader
)

import os
import re
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader
)

def clean_text(text: str) -> str:
    """Clean text formatting: fix broken line breaks, preserve paragraphs."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n{2,}', '<PARA>', text)   # mark paragraphs
    text = text.replace('\n', ' ')             # remove single line breaks
    text = text.replace('<PARA>', '\n\n')      # restore paragraphs
    text = re.sub(r' +', ' ', text)             # collapse spaces
    return text.strip()

def extract_pages_from_file(file_path: str) -> list[str]:
    """
    Extracts and returns a list of cleaned page texts from a PDF, TXT, or DOCX file.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext in [".docx", ".doc"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()
    # Each doc has: page_content, metadata (with page numbers for PDF)
    pages = [clean_text(doc.page_content) for doc in documents]

    return pages

