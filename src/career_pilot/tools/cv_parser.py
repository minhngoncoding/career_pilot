from typing import List, Tuple, Optional
from pypdf import PdfReader
from docx import Document


def parse_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages])
    return text


def parse_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def parse_txt(file_path: str) -> str:
    """Extract text from TXT file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def parse_resume(file_path: str) -> str:
    """Auto-detect format and parse resume."""
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    elif file_path.endswith(".txt"):
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def extract_sections(text: str) -> dict:
    """Identify CV sections from text."""
    sections = {}
    lines = text.split("\n")
    current_section = "header"
    current_content = []

    keywords = ["experience", "education", "skills", "certifications", "projects"]

    for line in lines:
        lower_line = line.lower().strip()
        if any(kw in lower_line for kw in keywords):
            if current_content:
                sections[current_section] = "\n".join(current_content)
            current_section = lower_line
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = "\n".join(current_content)

    return sections


def extract_contact_info(text: str) -> dict:
    """Extract name, email, phone from text."""
    import re

    info = {}
    lines = text.split("\n")[:5]

    for line in lines:
        email_match = re.search(r"[\w.-]+@[\w.-]+\.\w+", line)
        phone_match = re.search(r"[\d\s\-\+\(\)]{10,}", line)

        if email_match:
            info["email"] = email_match.group()
        if phone_match:
            info["phone"] = phone_match.group()

    return info
