import re
from typing import List, Optional

def clean_text(text: str) -> str:
    """
    Utility to clean and normalize resume or job text.
    Removes special characters, extra spaces, and converts to lowercase.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s,.@]', '', text)
    return text.strip()

def extract_skills_from_text(text: str, skill_keywords: List[str]) -> List[str]:
    """
    Simple skill extraction checking for presence of keywords in text.
    """
    found_skills = []
    text = text.lower()
    for skill in skill_keywords:
        if skill.lower() in text:
            found_skills.append(skill)
    return list(set(found_skills))

def format_salary(min_sal: Optional[int], max_sal: Optional[int], currency: str = "INR") -> str:
    """
    Helper to format salary ranges for responses.
    """
    if min_sal and max_sal:
        return f"{currency} {min_sal:,} - {max_sal:,}"
    elif min_sal:
        return f"{currency} {min_sal:,}+"
    elif max_sal:
        return f"Up to {currency} {max_sal:,}"
    return "Competitive"

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes using PyMuPDF (fitz).
    """
    import fitz # PyMuPDF
    text = ""
    try:
        # Open PDF from bytes
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

