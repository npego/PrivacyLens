# text_processing.py — HTML cleaning, PDF extraction, text segmentation

import io
import re

try:
    import pypdf
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from bs4 import BeautifulSoup
    BS4_SUPPORT = True
except ImportError:
    BS4_SUPPORT = False


def clean_html(raw: str) -> str:
    if BS4_SUPPORT:
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
    else:
        text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_from_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    raw_bytes = uploaded_file.read()
    if name.endswith(".pdf"):
        if not PDF_SUPPORT:
            return ""
        reader = pypdf.PdfReader(io.BytesIO(raw_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raw_str = raw_bytes.decode("utf-8", errors="replace")
    if name.endswith((".html", ".htm")):
        return clean_html(raw_str)
    return raw_str.strip()


def segment_text(text: str) -> list:
    paragraphs = re.split(r"\n{2,}", text)
    segments = []
    for para in paragraphs:
        para = para.strip()
        if len(para) < 30:
            continue
        if len(para) > 1500:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            current = ""
            for sent in sentences:
                if len(current) + len(sent) < 800:
                    current += " " + sent
                else:
                    if len(current.strip()) >= 30:
                        segments.append(current.strip())
                    current = sent
            if len(current.strip()) >= 30:
                segments.append(current.strip())
        else:
            segments.append(para)
    return segments