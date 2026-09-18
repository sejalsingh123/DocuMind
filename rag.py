import fitz

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_core.documents import (
    Document
)

import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_text_from_pdf(pdf_file):

    pdf_bytes = pdf_file.getvalue()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        if text.strip():

            pages.append({
                "text": text,
                "page": page_number + 1,
                "source": pdf_file.name
            })

    document.close()

    return pages


def create_chunks(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for page in pages:

        page_chunks = splitter.split_text(
            page["text"]
        )

        for chunk in page_chunks:

            chunks.append({
                "text": chunk,
                "page": page["page"],
                "source": page["source"]
            })

    return chunks

def create_vector_store(chunks):

    documents = []

    for chunk in chunks:

        documents.append(
            Document(
                page_content=chunk["text"],
                metadata={
                    "page": chunk["page"],
                    "source": chunk["source"]
                }
            )
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    return vector_store

def retrieve_documents(
    vector_store,
    question,
    k=4,
    threshold=1.2
):

    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

    documents = []

    for doc, score in results:

        if score <= threshold:

            doc.metadata["score"] = score

            documents.append(doc)

    return documents


def generate_answer(question, retrieved_documents):

    context = "\n\n".join(
        [
            f"[Source: {doc.metadata['source']} | "
            f"Page: {doc.metadata['page']}]\n"
            f"{doc.page_content}"
            for doc in retrieved_documents
        ]
    )

    prompt = f"""
You are DocuMind, an AI document research assistant.

Answer the user's question using ONLY the
provided document context.

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent facts.
3. If the answer is not supported by the context,
   say that you could not find the answer.
4. Mention the source document and page number
   that support your answer.
5. If multiple documents support the answer,
   mention all relevant sources.

DOCUMENT CONTEXT
================

{context}

================

USER QUESTION
================

{question}

================

ANSWER
================
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


def rewrite_question(question, chat_history):

    if not chat_history:
        return question

    history = "\n".join(
        [
            f"{message['role']}: {message['content']}"
            for message in chat_history[-6:]
        ]
    )

    prompt = f"""
You are a question rewriting assistant.

Convert the user's latest question into a
standalone question that can be understood
without conversation history.

Do not answer the question.

Conversation:
{history}

Latest question:
{question}

Return ONLY the rewritten standalone question.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()