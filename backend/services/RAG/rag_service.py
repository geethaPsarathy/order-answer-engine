from transformers import pipeline
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
from asyncio import gather
from services.llm_service import generate_dish_insight
from .search_service import faiss_only_search
from .indexing_service import index_data
import numpy as np
import torch

# Load Summarizer and Cross-Encoder for RAG Re-ranking
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


async def semantic_deduplication(texts, threshold=0.85):
    """
    Deduplicate reviews by filtering out similar text based on cosine similarity of embeddings.
    """
    embeddings = embedding_model.encode(texts, convert_to_tensor=False)
    similarities = cosine_similarity(embeddings)

    unique_texts = []
    seen_indices = set()

    for idx, text in enumerate(texts):
        if idx not in seen_indices:
            unique_texts.append(text)
            similar_indices = np.where(similarities[idx] > threshold)[0]
            seen_indices.update(similar_indices)

    print(f"[INFO] Deduplicated to {len(unique_texts)} unique reviews (semantic filtering).")
    return unique_texts


async def summarize_in_batches(texts, max_length=200):
    """
    Summarize a batch of texts by combining them and summarizing in chunks.
    """
    batch_size = 5
    summarized_reviews = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        combined_text = " ".join(batch)

        result = summarizer(
            combined_text,
            max_length=max_length,
            min_length=80,
            do_sample=False
        )
        summarized_reviews.append(result[0]["summary_text"])

    print(f"[INFO] Summarized {len(summarized_reviews)} batches.")
    return summarized_reviews


async def process_rag_pipeline(dish_name, yelp_reviews, reddit_comments):
    """
    Core RAG pipeline that retrieves, re-ranks, and summarizes Yelp reviews.
    """
    print("[INFO] Processing RAG pipeline...")

    # Index new data into FAISS
    if yelp_reviews or reddit_comments:
        index_data(yelp_reviews, reddit_comments)

    # Retrieve top matching reviews
    print(f"[INFO] Retrieving relevant reviews for '{dish_name}'...")
    retrieved_texts = faiss_only_search(dish_name)
    print(f"[INFO] Retrieved {len(retrieved_texts)} items.")

    if not retrieved_texts:
        print("[WARN] No relevant reviews from FAISS. Using all Yelp reviews instead.")
        retrieved_texts = yelp_reviews

    # Deduplicate and summarize
    deduplicated_reviews = await semantic_deduplication(retrieved_texts)
    summarized_reviews = await summarize_in_batches(deduplicated_reviews)

    # Pass to LLM for deeper insights
    final_insight = await generate_dish_insight(dish_name, summarized_reviews)

    return {
        "dish_name": dish_name,
        "insights": [final_insight],
        "source": "Hybrid (FAISS + Summarization)"
    }