import sys
import os
import time 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from rq import Queue
from redis import Redis
from rq.job import Job

# RAG imports
from app.rag.chunking import chunk_text
from app.services.embedding_service import model
from app.db.vector_db import create_faiss_index
from app.services.retriever import hybrid_retrieve
from app.rag.bm25 import build_bm25
from app.services.reranker_service import rerank
from app.services.qa_service import generate_answer

from app.workers.tasks import process_video

redis_conn = Redis()
q = Queue(connection=redis_conn)

st.title("🎥 AI Video Summarizer & Chat")

# 🔹 Input URL
url = st.text_input("Enter YouTube URL")

if st.button("Process Video"):
    if url:
        job = q.enqueue(process_video, url)
        st.session_state["job_id"] = job.id
        st.success(f"Job started! ID: {job.id}")

# 🔹 Check job status
if "job_id" in st.session_state:
    job = Job.fetch(st.session_state["job_id"], connection=redis_conn)

    status = job.get_status()
    st.write("Status:", status)

    if status == "finished":
        st.success("Processing complete!")

        result = job.result
        transcript = result["transcript"]

        st.subheader("Transcript Preview:")
        st.write(transcript[:500])

        st.session_state["transcript"] = transcript

    elif status == "failed":
        st.error("Job failed")

    else:
        st.warning("Still processing...")
        time.sleep(2)
        st.rerun()

# 🔥 CHAT SECTION
if "transcript" in st.session_state:

    st.subheader("💬 Chat with Video")

    query = st.text_input("Ask a question about the video")

    if query:
        text = st.session_state["transcript"]

        # 🔹 Chunk + embeddings
        chunks = chunk_text(text)
        embeddings = model.encode(chunks)
        index = create_faiss_index(embeddings)
        bm25 = build_bm25(chunks)

        # 🔹 Retrieve
        docs = hybrid_retrieve(query, model, index, chunks, bm25)

        if chunks[0] not in docs:
            docs.append(chunks[0])

        docs = rerank(query, docs)

        context = "\n".join(docs[:2])

        # 🔹 Answer
        answer = generate_answer(context, query)

        st.write("🤖 Answer:")
        st.write(answer)

# 🔥 SUMMARY SECTION
if "transcript" in st.session_state:

    st.subheader("🧾 Smart Summarization")

    summary_type = st.selectbox(
        "Choose summary type:",
        ["general", "beginner", "exam", "bullets", "detailed"]
    )

    if st.button("Generate Summary"):
        text = st.session_state["transcript"]

        with st.spinner("Generating summary..."):
            from app.services.summary_service import generate_summary
            summary = generate_summary(text, summary_type)

        st.write("📌 Summary:")
        st.write(summary)