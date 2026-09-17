import streamlit as st
import hashlib

from rag import (
    extract_text_from_pdf,
    create_chunks,
    create_vector_store,
    retrieve_documents,
    generate_answer,
    rewrite_question
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="DocuMind",
    page_icon="📚",
    layout="wide"
)


# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# TITLE
# =========================

st.title("📚 DocuMind")

st.subheader(
    "AI-powered PDF Research Assistant"
)


# =========================
# MULTIPLE PDF UPLOAD
# =========================

uploaded_files = st.file_uploader(
    "Upload your PDFs",
    type=["pdf"],
    accept_multiple_files=True
)


# =========================
# PROCESS PDFs
# =========================

if uploaded_files:

    combined_bytes = b""

    for pdf in uploaded_files:
        combined_bytes += pdf.getvalue()

    file_hash = hashlib.md5(
        combined_bytes
    ).hexdigest()


    if (
        "vector_store" not in st.session_state
        or
        st.session_state.get("file_hash")
        != file_hash
    ):

        with st.spinner(
            "Processing your documents..."
        ):

            all_pages = []

            for pdf in uploaded_files:

                pages = extract_text_from_pdf(
                    pdf
                )

                all_pages.extend(pages)


            chunks = create_chunks(
                all_pages
            )


            vector_store = create_vector_store(
                chunks
            )


            st.session_state.vector_store = (
                vector_store
            )

            st.session_state.file_hash = (
                file_hash
            )

            st.session_state.messages = []


    vector_store = (
        st.session_state.vector_store
    )


    st.success(
        f"✅ {len(uploaded_files)} documents "
        "ready for questions!"
    )


    with st.expander("📚 Uploaded Documents"):

        for pdf in uploaded_files:

            st.write(
                f"📄 {pdf.name}"
            )


    # =========================
    # CHAT HISTORY
    # =========================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    # =========================
    # QUESTION
    # =========================

    question = st.chat_input(
        "Ask a question about your documents..."
    )


    if question:

        with st.chat_message("user"):
            st.write(question)


        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # =========================
        # QUESTION REWRITE
        # =========================

        with st.spinner(
            "Understanding your question..."
        ):

            standalone_question = (
                rewrite_question(
                    question,
                    st.session_state.messages[:-1]
                )
            )


        # =========================
        # RETRIEVAL
        # =========================

        with st.spinner(
            "Searching your documents..."
        ):

            results = retrieve_documents(
                vector_store,
                standalone_question,
                k=4
            )


        # =========================
        # NO RESULTS
        # =========================

        if not results:

            answer = (
                "I couldn't find relevant "
                "information in your documents "
                "for this question."
            )


        # =========================
        # GENERATION
        # =========================

        else:

            with st.spinner(
                "Generating answer..."
            ):

                answer = generate_answer(
                    standalone_question,
                    results
                )


        # =========================
        # SHOW ANSWER
        # =========================

        with st.chat_message(
            "assistant"
        ):

            st.write(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # =========================
        # SOURCES
        # =========================

        # if results:

        #     st.subheader("📚 Sources")

        #     for i, doc in enumerate(results):

        #         page = doc.metadata["page"]

        #         source = doc.metadata["source"]

        #         score = doc.metadata.get(
        #             "score",
        #             None
        #         )

        #         with st.expander(
        #             f"📄 {source} — Page {page}"
        #         ):

        #             st.write(
        #                 doc.page_content
        #             )

        #             if score is not None:

        #                 st.caption(
        #                     f"FAISS distance: "
        #                     f"{score:.4f}"
        #                 )

