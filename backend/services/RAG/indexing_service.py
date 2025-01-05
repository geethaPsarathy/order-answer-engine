import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from asyncio import create_task , gather ,to_thread,wait_for

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384
faiss_index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
indexed_data = []
BATCH_SIZE = 100  # Batch size for indexing


async def async_index_data(yelp_reviews, reddit_comments):
    """
    Asynchronous FAISS indexing with batch processing.
    """
    global indexed_data

    data = [review["text"] for review in yelp_reviews] + \
           [comment["body"] for comment in reddit_comments]

    if not data:
        print("No data to index in FAISS.")
        return
        # Process data in batches asynchronously
    tasks = [
        process_and_index_batch(data[i:i + BATCH_SIZE])
        for i in range(0, len(data), BATCH_SIZE)
    ]

    # awai gather(*tasks)
    await wait_for(gather(*tasks), timeout=300)
    print(f"Total items indexed: {len(indexed_data)}")
    
    # Process data in batches
    # for i in range(0, len(data), BATCH_SIZE):
    #     batch = data[i:i + BATCH_SIZE]
    #     embeddings = embedding_model.encode(batch, convert_to_tensor=False)
    #     faiss_index.add(np.array(embeddings))
    #     indexed_data.extend(batch)
    #     print(f"Indexed batch {i//BATCH_SIZE + 1}/{-(-len(data) // BATCH_SIZE)}. Total items: {len(indexed_data)}.")

async def process_and_index_batch(batch):
    """
    Process embeddings and add them to FAISS asynchronously.
    """
    global indexed_data

    # Generate embeddings asynchronously
    embeddings = await to_thread(embedding_model.encode, batch, convert_to_tensor=False)
    
    # Perform FAISS indexing in a separate thread
    await to_thread(faiss_index.add, np.array(embeddings))

    # Update indexed data
    indexed_data.extend(batch)
    print(f"Indexed {len(batch)} items. Total items: {len(indexed_data)}.")

async def index_data(yelp_reviews, reddit_comments):
    """
    Trigger FAISS indexing as a background task.
    """
    print("Triggering FAISS indexing...")
    await create_task(async_index_data(yelp_reviews, reddit_comments))


def get_indexed_data():
    """
    Retrieve the indexed data.
    """
    print(f"Indexed data size: {len(indexed_data)} items.")
    return indexed_data


def get_faiss_index():
    """
    Retrieve FAISS index.
    """
    print(f"FAISS index size: {faiss_index.ntotal} items.")
    return faiss_index


async def update_faiss_index(yelp_reviews, reddit_comments):
    global indexed_data

    data = [review["text"] for review in yelp_reviews] + \
           [comment["body"] for comment in reddit_comments]

    print(f"Indexing {len(data)} new items...")

    if not data:
        return

    embeddings = embedding_model.encode(data, convert_to_tensor=False)
    faiss_index.add(np.array(embeddings))
    indexed_data.extend(data)
    print(f"Indexed {len(data)} new items. FAISS index size: {faiss_index.ntotal} items.")
