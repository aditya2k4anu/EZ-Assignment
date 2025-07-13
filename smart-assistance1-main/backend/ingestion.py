import nltk
import fitz  # PyMuPDF
from nltk.tokenize import sent_tokenize

# Force NLTK to use the correct download path
nltk.data.path.append("C:/Users/namra/AppData/Roaming/nltk_data")

def extract_text(file):
    ext = file.name.split(".")[-1].lower()
    if ext == "pdf":
        raw_text = extract_text_from_pdf(file)
    elif ext == "txt":
        raw_text = file.read().decode("utf-8")
    else:
        return ""
    return preprocess_text(raw_text)  # ✅ Preprocess layout text


def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))  # Sort top-to-bottom, left-to-right
        for b in blocks:
            line = b[4].strip()
            if line:
                text += line + "\n"
    return text


def preprocess_text(text):
    lines = text.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Add logic to pair label + value in one line
        if line == "Student Name" and i + 1 < len(lines):
            new_lines.append(f"Student Name: {lines[i + 1].strip()}")
            i += 2
        elif line == "Father's Name" and i + 1 < len(lines):
            new_lines.append(f"Father's Name: {lines[i + 1].strip()}")
            i += 2
        elif line == "Mother's Name" and i + 1 < len(lines):
            new_lines.append(f"Mother's Name: {lines[i + 1].strip()}")
            i += 2
        elif line == "Address" and i + 1 < len(lines):
            address = [lines[i + 1].strip()]
            j = i + 2
            while j < len(lines) and lines[j].strip() != "":
                address.append(lines[j].strip())
                j += 1
            new_lines.append(f"Address: {' '.join(address)}")
            i = j
        else:
            new_lines.append(line)
            i += 1
    return "\n".join(new_lines)


def chunk_text(text, chunk_size=500):
    sentences = sent_tokenize(text)
    chunks = []
    current = ""

    for sent in sentences:
        if len(current) + len(sent) <= chunk_size:
            current += " " + sent
        else:
            chunks.append(current.strip())
            current = sent
    if current:
        chunks.append(current.strip())

    return [{"cid": f"C{i}", "text": chunk} for i, chunk in enumerate(chunks)]
