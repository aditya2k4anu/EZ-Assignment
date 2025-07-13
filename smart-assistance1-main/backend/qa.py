import re
from backend.llm import call_openai
from backend.embeddings import VectorStore
from backend.ingestion import chunk_text
from backend import nltk_setup  # Make sure punkt is ready
from nltk.tokenize import sent_tokenize

def ask_question(text, question):
    # Clean up any noisy spacing
    text = re.sub(r'\s+', ' ', text).strip()

    # Chunk and embed
    chunks = chunk_text(text)
    store = VectorStore(chunks)
    top_contexts = store.query(question, k=3)

    # Format context with clear separators
    context_str = "\n---\n".join([f"[Chunk {i+1}]: {c['text']}" for i, c in enumerate(top_contexts)])

    # Improved prompt engineering
    prompt = f"""
You are a precise document assistant.

Answer ONLY with the exact value requested from the context below.

- If asked about a specific field (e.g., Student Name), return ONLY that field’s value, no extra text or labels.
- If the question is ambiguous (e.g., "what is your name?"), assume it refers to the student’s name.
- If the answer is not found exactly, reply with:
"Not found in the document."

Context:
{context_str}

Question: {question}
Answer:
"""

    answer = call_openai(prompt)
    return answer.strip(), context_str
