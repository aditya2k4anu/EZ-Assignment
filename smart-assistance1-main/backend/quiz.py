from backend.llm import call_openai
from backend.embeddings import VectorStore
from backend.ingestion import chunk_text
from backend import nltk_setup  # Ensures 'punkt' tokenizer is available
import re

# ---------------------- Question Generator ----------------------

def generate_questions(text, n=3):
    # Clean the text and truncate to first 1000 characters to avoid prompt overflow
    clean_text = re.sub(r"\s+", " ", text.strip())[:1000]

    # Improved prompt to reduce repetition and improve diversity
    prompt = f"""
You are a helpful assistant.

Generate {n} unique, factual, and concise questions based ONLY on the document below. Each question should cover a different point. Do NOT repeat the same question or phrasing.

Document:
\"\"\"
{clean_text}
\"\"\"

Return only the questions as a numbered list starting from 1.
Example:
1. ...
2. ...
3. ...

Questions:
"""

    # Call LLM
    output = call_openai(prompt)

    # Optional debug
    print("Model raw output:\n", output)

    return parse_questions(output.strip())

# ---------------------- Answer Grader ----------------------

def grade_answers(questions, answers, text):
    # Normalize and chunk the text
    clean_text = re.sub(r"\s+", " ", text.strip())
    chunks = chunk_text(clean_text)
    store = VectorStore(chunks)

    feedback = []

    # Loop through each question and answer
    for q, a in zip(questions, answers):
        context = store.query(q, k=3)
        context_str = "\n---\n".join([f"[Chunk {i+1}]: {c['text']}" for i, c in enumerate(context)])

        prompt = f"""
You are a strict but helpful evaluator.

Use ONLY the context below to evaluate the user's answer to the question.

Provide a short evaluation with a clear justification.
If the answer is not present in the context, say:
"Not found in the document."

Context:
{context_str}

Question: {q}
User's Answer: {a}

Evaluation:
"""
        fb = call_openai(prompt)
        feedback.append(fb.strip())

    return feedback

# ---------------------- Question Parser ----------------------

def parse_questions(raw_text):
    """
    Parses and deduplicates questions from a numbered list (1., 2), etc).
    """
    lines = raw_text.split('\n')
    questions = []
    seen = set()
    for line in lines:
        # Match formats like 1. or 1)
        if re.match(r"^\d+[\.\)]\s*", line):
            question = re.sub(r"^\d+[\.\)]\s*", "", line).strip()
            if question and question.lower() not in seen:
                questions.append(question)
                seen.add(question.lower())  # case-insensitive deduplication
    return questions
