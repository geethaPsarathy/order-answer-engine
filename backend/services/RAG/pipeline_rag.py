from transformers import pipeline
from sentence_transformers import CrossEncoder
from asyncio import gather

from services.llm_service import generate_dish_insight
from .search_service import hybrid_search
from .indexing_service import index_data
import torch

# Load Summarizer and Cross-Encoder for RAG Re-ranking
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')


async def summarize_texts_in_steps(texts, max_length=200):
    """
    Summarize a batch of texts in two steps:
    - Summarize long reviews individually.
    - Concatenate summarized reviews and summarize again for concise insights.
    """
    if not texts:
        return []

    print(f"[INFO] Summarizing {len(texts)} texts...")
    summarized_reviews = []

    # Step 1: Summarize Each Review Separately (if long)
    for text in texts:
        if len(text.split()) > 40:
            result = summarizer(text, max_length=150, min_length=50, do_sample=False)
            summarized_reviews.append(result[0]['summary_text'])
        else:
            summarized_reviews.append(text)

    # Step 2: Combine and Summarize Again for Final Insights
    combined_text = " ".join(summarized_reviews)
    if len(combined_text.split()) > 150:
        print("[INFO] Performing final summarization pass...")
        final_summary = summarizer(combined_text, max_length=max_length, min_length=80, do_sample=False)
        return [final_summary[0]['summary_text']]
    
    return summarized_reviews


async def process_rag_pipeline(dish_name, yelp_reviews, reddit_comments):
    """
    Core RAG pipeline that retrieves, re-ranks, and summarizes Yelp reviews.
    """
    print("[INFO] Processing RAG pipeline...")

    if yelp_reviews or reddit_comments:
        print("[INFO] Updating FAISS index...")
        index_data(yelp_reviews, reddit_comments)

    # Perform Hybrid Retrieval
    print(f"[INFO] Retrieving relevant reviews for '{dish_name}'...")
    retrieved_texts = hybrid_search(dish_name)
    print(f"[INFO] Retrieved {len(retrieved_texts)} items.")

    if not retrieved_texts:
        print("[WARN] No relevant reviews from FAISS. Using all Yelp reviews instead.")
        retrieved_texts = yelp_reviews  # Fallback to all reviews if FAISS fails

    # Re-rank Retrieved Reviews using Cross-Encoder
    print("[INFO] Re-ranking retrieved texts...")
    responses = [[dish_name, text] for text in retrieved_texts]
    scores = cross_encoder.predict(responses)
    ranked_texts = sorted(zip(retrieved_texts, scores), key=lambda x: x[1], reverse=True)
    top_texts = [text for text, _ in ranked_texts[:5]]  # Take Top 5

    # Summarize and Generate Insights
    try:
        print(f"[INFO] Summarizing top {len(top_texts)} texts...")
        summarized_reviews = await summarize_texts_in_steps(top_texts)
        print(f"[INFO] Summarization complete.")
    except Exception as e:
        print(f"[ERROR] Summarization failed: {str(e)}")
        summarized_reviews = top_texts  # Fallback to raw reviews if summarization fails

    
    return {
        "dish_name": dish_name,
        "insights": summarized_reviews,
        "source": "Hybrid (FAISS + Summarization)"
    }
