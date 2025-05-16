# Resume Screening Assistance 💼🤖

A Streamlit-based AI tool to help HR professionals quickly screen resumes against a given job description using NLP and vector similarity search.

## 🔍 Features

* Upload multiple PDF resumes
* Paste a job description
* Choose how many relevant resumes to return
* Uses HuggingFace embeddings & Pinecone vector DB for similarity search
* Provides summary of each matched resume using an LLM

## 🛠️ Tech Stack

* Python 🐍
* Streamlit 🌐 (Frontend)
* LangChain ⚙️ (Document handling & summarization)
* HuggingFace Embeddings 🧠
* Pinecone 🌲 (Vector database)
* Groq (LLM API for summarization)
* dotenv 🔐 (Environment variables)

## 🚀 How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/Zoya28/Resume_screening_app.git
cd Resume-screening-app
```

### 2. Set Up Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root directory and add your Pinecone & Groq API keys:

```
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the App

```bash
streamlit run main.py
```

## 📂 Project Structure

```
resume-screening-app/
│
├── main.py                # Streamlit frontend
├── backend.py             # Helper functions and logic
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not included in repo)
└── README.md              # You're reading it!
```


## ✅ To-Do

* Add login/authentication
* Store matched results for future use
* Improve summary output with better prompts

## 🙌 Acknowledgements

* Streamlit for easy app development
* Pinecone for fast and scalable vector search
* HuggingFace & LangChain for embedding and summarization power


