import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from .indexing_service import get_faiss_index, get_indexed_data
from utils.bm25_utils import search_bm25

# Models
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Weights for hybrid search
BM25_WEIGHT = 0.6
FAISS_WEIGHT = 0.4


def rerank_results(query, results):
    """
    Re-rank results using a cross-encoder model.
    """
    if not results:
        return []

    # Create pairs of (query, result) for re-ranking
    pairs = [[query, res] for res in results]

    # Predict relevance scores
    scores = cross_encoder.predict(pairs)

    # Sort results by descending score
    reranked_results = [
        result for result, _ in sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    ]

    print(f"Re-ranked {len(reranked_results)} items.")
    return reranked_results


def hybrid_search(query, k=5):
    """
    Perform hybrid search using FAISS and BM25, followed by re-ranking.
    """
    faiss_index = get_faiss_index()
    indexed_data = get_indexed_data()

    print("Performing hybrid search...")

    # # BM25 Search
    # print("Searching BM25 index...")
    # bm25_indices, bm25_results = search_bm25(query, k)
    # print(f"BM25 results: {len(bm25_results)} items.")

    # # FAISS Search
    # if faiss_index.ntotal == 0:
    #     print("FAISS index is empty. Returning BM25 results only.")
    #     return bm25_results

    print("Encoding query for FAISS search...")
    query_embedding = embedding_model.encode([query], convert_to_tensor=False)
    D, I = faiss_index.search(np.array(query_embedding), k)
    faiss_results = [indexed_data[i] for i in I[0] if i < len(indexed_data)]
    print(f"FAISS results: {len(faiss_results)} items.")

    # Combine and Deduplicate
    combined_results = list(dict.fromkeys(faiss_results))

    # Re-rank Combined Results
    reranked_results = rerank_results(query, combined_results)

    return reranked_results


def faiss_only_search(query, k=5):
    """
    Perform FAISS search only (BM25 temporarily commented out).
    """
    faiss_index = get_faiss_index()
    indexed_data = get_indexed_data()

    print("Encoding query for FAISS search...")
    faiss_results, faiss_scores = [], []
    
    # Perform FAISS Search
    if faiss_index.ntotal > 0:
        query_embedding = embedding_model.encode([query], convert_to_tensor=False)
        D, I = faiss_index.search(np.array(query_embedding), k)
        faiss_results = [indexed_data[i] for i in I[0] if i < len(indexed_data)]
        reranked = rerank_results(query, faiss_results)
    else:
        print("FAISS index is empty. No results found.")
    
    print(f"FAISS search returned {len(faiss_results)} items.")
    return reranked


