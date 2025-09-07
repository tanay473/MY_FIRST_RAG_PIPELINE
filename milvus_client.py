# -*- coding: utf-8 -*-
"""
Handles all interactions with the Milvus vector database,
now configured for Zilliz Cloud.
"""
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import config

class MilvusClient:
    """A client to manage connections and operations with Zilliz Cloud."""
    def __init__(self):
        """Initializes the client and connects to Zilliz Cloud."""
        self.collection = None
        try:
            if not config.ZILLIZ_URI or not config.ZILLIZ_TOKEN:
                raise ValueError("ZILLIZ_URI and ZILLIZ_TOKEN must be set in your .env file.")
            connections.connect("default", uri=config.ZILLIZ_URI, token=config.ZILLIZ_TOKEN)
            print(f"Successfully connected to Zilliz Cloud.")
        except Exception as e:
            print(f"Failed to connect to Zilliz Cloud: {e}")
            raise

    def get_or_create_collection(self):
        """
        Gets the collection if it exists, otherwise creates a new one.
        Also ensures the collection has the correct index.
        """
        if utility.has_collection(config.COLLECTION_NAME):
            print(f"Collection '{config.COLLECTION_NAME}' already exists. Loading it.")
            self.collection = Collection(config.COLLECTION_NAME)
            if not self.collection.has_index():
                 print("Index not found on the 'embeddings' field. Creating one now...")
                 self.create_index()
            else:
                 print("Index already exists.")
        else:
            print(f"Collection '{config.COLLECTION_NAME}' does not exist. Creating it.")
            fields = [
                FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
                # The max_length for a VARCHAR field in Milvus is 65535. This cannot be increased.
                # The document loader must ensure that no text chunk exceeds this limit.
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=config.EMBEDDING_DIM)
            ]
            schema = CollectionSchema(fields, "RAG demo collection for Zilliz")
            
            print(f"Creating collection: {config.COLLECTION_NAME}")
            self.collection = Collection(config.COLLECTION_NAME, schema)
            self.create_index()

        return self.collection

    def create_index(self):
        """Creates an index based on the parameters in config.py."""
        if not self.collection:
            raise Exception("Collection is not initialized. Call get_or_create_collection first.")
            
        print(f"Creating index with the following parameters: {config.INDEX_PARAMS}")
        self.collection.create_index(
            field_name="embeddings",
            index_params=config.INDEX_PARAMS
        )
        print("Index created successfully.")
        
    def disconnect(self):
        """Disconnects from Milvus."""
        connections.disconnect("default")
        print("Disconnected from Zilliz Cloud.")

