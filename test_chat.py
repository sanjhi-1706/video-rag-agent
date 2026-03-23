from app.rag.chunking import chunk_text
from app.services.embedding_service import model
from app.db.vector_db import create_faiss_index
from app.services.retriever import hybrid_retrieve
from app.rag.bm25 import build_bm25
from app.services.reranker_service import rerank
from app.services.qa_service import generate_answer

# 🔹 Detect question type
def is_general_question(query):
    keywords = ["about", "summary", "summarize", "overview", "main idea"]
    return any(word in query.lower() for word in keywords)

# 🔹 Load transcript
file_path = "data/transcripts/4Gg4tzI03vw.txt"

with open(file_path, "r") as f:
    transcript = f.read()

# 🔥 TEMP BLIP captions (for now)
captions = [
    "a person speaking on stage",
    "a presentation slide is shown",
    "audience listening to speaker"
]

# 🔥 MERGE TRANSCRIPT + VISUAL CONTEXT
visual_text = "\n".join(captions)

text = f"""
Transcript:
{transcript}

Visual Context:
{visual_text}
"""

# 🔹 Chunk
chunks = chunk_text(text)

print(f"📦 Total chunks: {len(chunks)}")

# 🔹 Build BM25
bm25 = build_bm25(chunks)

# 🔹 Embeddings
embeddings = model.encode(chunks)

# 🔹 FAISS index
index = create_faiss_index(embeddings)

print("🚀 Hybrid Multimodal RAG Chat Ready!")

# 🔹 Chat loop
while True:
    query = input("\nAsk question (or 'exit'): ")

    if query.lower() == "exit":
        break

    # 🔥 SMART ROUTING
    if is_general_question(query):
        print("\n🧠 Using FULL context (global question)")
        context = text[:2000]
    else:
        docs = hybrid_retrieve(query, model, index, chunks, bm25)

        # Always include intro
        if chunks[0] not in docs:
            docs.append(chunks[0])

        docs = rerank(query, docs)

        context = "\n".join(docs[:2])

    print("\n🔍 Context Preview:\n", context[:300], "...")

    # 🔹 Generate answer
    answer = generate_answer(context, query)

    print("\n🤖 Answer:", answer)