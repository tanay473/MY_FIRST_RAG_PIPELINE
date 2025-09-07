# -*- coding: utf-8 -*-
"""
Handles the ingestion of document chunks into the Milvus collection.
Now with batching for improved performance and a progress bar.
"""
import uuid
from tqdm import tqdm # Import tqdm for the progress bar

def ingest_documents(collection, documents, embedding_model, batch_size=128):
    """
    Ingests a list of document chunks into the Milvus collection in batches.

    Args:
        collection (Collection): The Milvus collection object.
        documents (list[str]): A list of document text chunks.
        embedding_model: The sentence transformer model for creating embeddings.
        batch_size (int): The number of documents to process in each batch.
    """
    print(f"Starting ingestion of {len(documents)} document chunks in batches of {batch_size}...")

    # Use tqdm to create a progress bar
    for i in tqdm(range(0, len(documents), batch_size), desc="Ingesting Batches"):
        # Get the current batch of text chunks
        batch_texts = documents[i:i + batch_size]
        
        # 1. Generate embeddings for the entire batch at once
        batch_embeddings = embedding_model.encode(batch_texts).tolist()
        
        # 2. Prepare entities for batch insertion
        entities = [
            {
                "pk": str(uuid.uuid4()),
                "text": text,
                "embeddings": emb
            }
            for text, emb in zip(batch_texts, batch_embeddings)
        ]
        
        # 3. Insert the batch into the collection
        try:
            collection.insert(entities)
        except Exception as e:
            print(f"An error occurred during batch insertion: {e}")
            # Optional: decide if you want to stop or continue on error
            continue

    # After insertion, flush the data to make it searchable
    print("Flushing data to make it searchable...")
    collection.flush()
    print("Ingestion and flushing complete.")

