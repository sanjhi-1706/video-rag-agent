import numpy as np
from app.rag.bm25 import bm25_search

def hybrid_retrieve(query, model, index, chunks, bm25, k=3):

    # 🔹 FAISS (semantic)
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    faiss_results = [chunks[i] for i in I[0]]

    # 🔹 BM25 (keyword)
    bm25_results = bm25_search(query, bm25, chunks, k)

    # 🔹 Combine (remove duplicates)
    combined = list(set(faiss_results + bm25_results))

    return combined