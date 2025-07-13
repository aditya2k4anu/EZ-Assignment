import streamlit as st
from backend.ingestion import extract_text, chunk_text
from backend.qa import ask_question
from backend.quiz import generate_questions, grade_answers

st.set_page_config(page_title="Smart Research Assistant")

def generate_summary(text):
    return text[:1000][:150].strip() + "..."

def main():
    st.title("Smart Research Assistant")
    st.write("Upload a PDF or TXT file to get started.")

    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt"])

    if uploaded_file:
        text = extract_text(uploaded_file)
        st.success("✅ File uploaded successfully!")

        st.subheader("📄 Auto Summary (150 words)")
        st.info(generate_summary(text))

        mode = st.radio("Choose Mode", ["Ask Anything", "Challenge Me"])

        if mode == "Ask Anything":
            user_q = st.text_input("Ask a question about the document")
            if user_q:
                with st.spinner("Thinking..."):
                    answer, context = ask_question(text, user_q)
                    st.markdown(f"**Answer:** {answer}")
                    st.markdown("**Justification:**")
                    st.code(context)

        elif mode == "Challenge Me":
            st.write("🧠 Generating questions...")
            questions = generate_questions(text)
            user_answers = []

            for i, q in enumerate(questions):
                user_answer = st.text_input(f"Q{i+1}: {q}", key=f"q{i}")
                user_answers.append(user_answer)

            if st.button("Submit Answers"):
                with st.spinner("Evaluating..."):
                    feedback = grade_answers(questions, user_answers, text)
                    for i, f in enumerate(feedback):
                        st.markdown(f"**Q{i+1} Feedback:** {f}")

if __name__ == "__main__":
    main()
