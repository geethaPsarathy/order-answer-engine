from rank_bm25 import BM25Okapi

bm25_index = None  # BM25 instance
indexed_texts = []  # Store text data for BM25


def build_bm25_index(yelp_reviews, reddit_comments):
    """
    Build or update BM25 index from Yelp and Reddit data.
    """
    global bm25_index, indexed_texts

    try:
        # Prepare and tokenize data
        new_texts = [review["text"] for review in yelp_reviews] + \
                    [comment["body"] for comment in reddit_comments]
        
        if not new_texts:
            print("[INFO] No new data to index for BM25.")
            return
        
        # Tokenize the new data
        tokenized_corpus = [text.split() for text in new_texts]
        
        if bm25_index is None:
            # Create BM25 index if it doesn't exist
            bm25_index = BM25Okapi(tokenized_corpus)
            indexed_texts.extend(new_texts)
            print(f"[INFO] BM25 index built with {len(indexed_texts)} items.")
        else:
            # Update the existing index
            indexed_texts.extend(new_texts)
            bm25_index = BM25Okapi([text.split() for text in indexed_texts])
            print(f"[INFO] BM25 index updated. Total items: {len(indexed_texts)}.")

    except Exception as e:
        print(f"[ERROR] Failed to build BM25 index: {str(e)}")


def search_bm25(query, k=5):
    """
    Perform BM25 search for keyword matching.
    """
    if not bm25_index:
        raise ValueError("BM25 index is empty. Please index data first.")
    
    try:
        # Tokenize the query
        tokenized_query = query.split()
        
        # Perform BM25 scoring
        scores = bm25_index.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        
        # Retrieve top-k results
        results = [indexed_texts[i] for i in top_indices]
        print(f"[INFO] BM25 search returned {len(results)} results for query '{query}'.")
        return top_indices, results

    except Exception as e:
        print(f"[ERROR] BM25 search failed: {str(e)}")
        return [], []
