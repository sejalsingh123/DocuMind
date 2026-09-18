# 📄 DocuMind

**DocuMind** is an AI-powered document research assistant that allows users to upload PDF documents and ask questions about their content.

It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the uploaded documents and generate answers using Google Gemini.

🔗 **Live Demo:** https://documind-oesre93tvcu2uebd6ck3xt.streamlit.app/

🔗 **GitHub Repository:** https://github.com/sejalsingh123/DocuMind

---

## ✨ Features

* 📄 Upload PDF documents
* 📚 Multiple PDF support
* 🔍 RAG-based document retrieval
* 🤖 AI-generated answers using Google Gemini
* 💬 Conversational follow-up questions
* 📑 Page-based document references
* 🧠 Automatic question rewriting for contextual conversations

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini API**
* **LangChain**
* **ChromaDB**
* **Sentence Transformers**
* **PyPDF**

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sejalsingh123/DocuMind.git
cd DocuMind
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Get your API key from **Google AI Studio**.

### 5. Run the application

```bash
streamlit run app.py
```


---

## 💡 How to Use

1. Open DocuMind.
2. Upload one or more PDF documents.
3. Wait for the documents to be processed.
4. Ask a question about the uploaded documents.
5. DocuMind retrieves relevant information and generates an answer.
6. Continue asking follow-up questions.

---

## 🔐 Environment Variables

| Variable         | Description           |
| ---------------- | --------------------- |
| `GEMINI_API_KEY` | Google Gemini API key |

For Streamlit Cloud deployment, add the API key through **Secrets** instead of committing the `.env` file.


---

## 🌐 Deployment

DocuMind is deployed using **Streamlit Community Cloud**.

### Deployment steps

1. Push the project to GitHub.
2. Connect the repository to Streamlit Community Cloud.
3. Select `app.py` as the main file.
4. Add `GEMINI_API_KEY` under Streamlit Secrets.
5. Deploy the application.

### Live Application

👉 https://documind-oesre93tvcu2uebd6ck3xt.streamlit.app/

---

## 📁 Project Structure

```text
DocuMind/
│
├── app.py
├── rag.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📜 License

This project is created for learning and demonstration purposes.
