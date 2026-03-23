from app.services.stt_service import transcribe
from app.rag.chunking import chunk_text
from app.services.embedding_service import get_embeddings
from app.db.vector_db import create_faiss_index

audio_path = input("Enter audio path: ")

# Step 1: Transcribe
text, _ = transcribe(audio_path)

# Step 2: Chunk
chunks = chunk_text(text)

print(f"\n📦 Total chunks: {len(chunks)}")

# Step 3: Embeddings
embeddings = get_embeddings(chunks)

print("🧠 Embeddings created")

# Step 4: FAISS index
index = create_faiss_index(embeddings)

print("📚 FAISS index ready")