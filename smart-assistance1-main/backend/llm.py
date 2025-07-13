from transformers import pipeline

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)

def call_openai(prompt, max_tokens=256):
    result = qa_pipeline(prompt, max_new_tokens=max_tokens, do_sample=False)
    return result[0]["generated_text"]
