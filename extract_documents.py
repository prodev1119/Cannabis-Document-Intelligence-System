# Sample municipal documents extraction utilities for cannabis business relevance testing
# These represent realistic city documents that would be found in municipal systems

import os
import pdfplumber
from docx import Document
from typing import Dict, List


def process_pdf_documents(folder_path: str = "docs") -> Dict[str, str]:
    """
    Find all PDFs in a folder, extract text, and return a dictionary.

    Args:
        folder_path: The path to the folder containing PDFs.

    Returns:
        A dictionary where keys are filenames and values are the extracted text.
    """
    pdf_texts = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        pdf_texts[file] = text
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
    return pdf_texts


def extract_all_documents(folder_path: str = "docs") -> Dict[str, str]:
    """
    Recursively find and extract text from all .pdf, .docx, and .txt files in the given folder.
    Skips .doc files and prints a warning.
    Returns a dict of {filename: content}.
    """
    supported_exts = [".pdf", ".docx", ".txt"]
    documents = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            file_path = os.path.join(root, file)
            if ext in supported_exts:
                try:
                    if ext == ".pdf":
                        with pdfplumber.open(file_path) as pdf:
                            text = ""
                            for page in pdf.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n"
                        documents[file] = text
                    elif ext == ".docx":
                        doc = Document(file_path)
                        text = "\n".join([para.text for para in doc.paragraphs])
                        documents[file] = text
                    elif ext == ".txt":
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            documents[file] = f.read()
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
            elif ext == ".doc":
                print(f"Skipping unsupported DOC file (requires textract or antiword): {file_path}")
    return documents 