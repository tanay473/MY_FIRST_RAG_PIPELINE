# -*- coding: utf-8 -*-
"""
Main script to run the RAG pipeline.
Orchestrates the ingestion, retrieval, and generation steps.
"""
import config
from pymilvus import utility  # Import the utility module
from milvus_client import MilvusClient
from embedding import get_embedding_model
from ingestion import ingest_documents
from retriever import Retriever
from generator import Generator
from document_loader import load_and_split_documents

def main():
    """The main function to execute the RAG pipeline."""
    # --- 1. Setup ---
    milvus_cli = MilvusClient()

    # --- 2. Re-ingestion Logic ---
    # Drop the collection if it exists to ensure fresh ingestion of all current documents
    if utility.has_collection(config.COLLECTION_NAME):
        print(f"Collection '{config.COLLECTION_NAME}' found. Dropping for re-ingestion.")
        utility.drop_collection(config.COLLECTION_NAME)
    
    print("Creating a new collection for ingestion.")
    collection = milvus_cli.get_or_create_collection()
    embedding_model = get_embedding_model()
    
    # This block will now run every time to ingest all files from the docs directory
    print("Starting document ingestion...")
    documents_to_ingest = load_and_split_documents(config.DOCS_DIR)
    
    if documents_to_ingest:
        ingest_documents(collection, documents_to_ingest, embedding_model)
        collection.load()  # Load collection into memory for searching
        print(f"Ingestion complete. Collection now has {collection.num_entities} entities.")
    else:
        print("No documents found to ingest. Exiting.")
        return  # Exit if there's nothing to process
    
    # --- 3. RAG Loop ---
    retriever = Retriever(collection, embedding_model)
    generator = Generator()
    
    try:
        while True:
            print("\n" + "="*50)
            query = input("Enter your query (or 'exit' to quit): ")
            if query.lower() == 'exit':
                break
                
            # 1. Retrieve
            retrieved_context = retriever.search(query)
            
            print("\n--- Retrieved Context ---")
            for doc in retrieved_context:
                print(f"- {doc}")
            print("------------------------")
            
            # 2. Generate
            final_answer = generator.generate_response(query, retrieved_context)
            
            print("\n--- Final Answer ---")
            print(final_answer)
            print("--------------------")
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # --- 4. Cleanup ---
        milvus_cli.disconnect()
        print("Pipeline finished.")

if __name__ == "__main__":
    main()

