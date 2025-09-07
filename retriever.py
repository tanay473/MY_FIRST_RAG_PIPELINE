# -*- coding: utf-8 -*-
"""
Handles the retrieval of documents from Milvus.
"""
import config

class Retriever:
    """A class to retrieve relevant documents from Milvus."""
    def __init__(self, collection, embedding_model):
        self.collection = collection
        self.embedding_model = embedding_model
        # Ensure the collection is loaded into memory for searching
        self.collection.load()

    def search(self, query_text):
        """
        Searches for the most relevant documents for a given query.
        """
        print(f"\nSearching for top {config.TOP_K} documents similar to: '{query_text}'")
        query_embedding = self.embedding_model.encode([query_text])
        
        results = self.collection.search(
            data=query_embedding,
            anns_field="embeddings",
            param=config.SEARCH_PARAMS,
            limit=config.TOP_K,
            expr=None,
            output_fields=['text']
        )
        
        retrieved_texts = [hit.entity.get('text') for hit in results[0]]
        return retrieved_texts

