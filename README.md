# 📄 Smart Research Assistant

Smart Research Assistant is a simple and powerful tool that helps you **summarize research papers** (PDF or text files) using AI. Just upload your file and get a short, clear summary in seconds.

---

## 🚀 Features

- 📁 Upload `.pdf` or `.txt` research files  
- 🧠 Get instant AI-generated summaries  
- 🤖 Powered by Hugging Face models  
- 🖥️ Simple and clean user interface using Streamlit

---

## 🛠️ Tech Stack

- Python 🐍  
- Streamlit 🧾  
- Hugging Face 🤗  
- dotenv (for keeping your API keys safe)

---

## 📦 How to Run

1. **Clone this repository**  
```bash
git clone https://github.com/aditya2k4anu/EZ-Assignment.git
cd EZ-Assignment
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows
Install the required packages

bash
Copy
Edit
pip install -r requirements.txt
Add your API keys

Create a .env file in the root folder and add your keys:

env
Copy
Edit
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_key  # if used
Run the app

bash
Copy
Edit
streamlit run app.py
