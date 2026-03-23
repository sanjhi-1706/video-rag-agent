from rank_bm25 import BM25Okapi

def build_bm25(chunks):
    tokenized_chunks = [chunk.split() for chunk in chunks]
    return BM25Okapi(tokenized_chunks)


def bm25_search(query, bm25, chunks, k=3):
    tokenized_query = query.split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )

    return [chunks[i] for i, _ in ranked[:k]]