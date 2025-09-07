# -*- coding: utf-8 -*-
"""
Configuration file for the RAG pipeline.
Loads settings from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Zilliz Cloud (Milvus) Configuration ---
ZILLIZ_URI = os.getenv("ZILLIZ_URI")
ZILLIZ_TOKEN = os.getenv("ZILLIZ_TOKEN")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_documents")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 768))

# HNSW is a graph-based index that is good for speed/accuracy tradeoffs
INDEX_PARAMS = {
    "metric_type": "IP",  # Inner Product for similarity
    "index_type": "HNSW",
    "params": {"M": 16, "efConstruction": 200}
}

# Search parameters for HNSW
SEARCH_PARAMS = {
    "metric_type": "IP",
    "params": {"ef": 50}
}

TOP_K = 3

# --- Embedding Model Configuration ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", 'all-mpnet-base-v2')

# --- LM Studio Configuration ---
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_STUDIO_API_KEY = "not-needed"
LM_STUDIO_MODEL = "local-model"  # This field is ignored by LM Studio but required by the API

# --- Document Source ---
# The pipeline will process all .pdf and .txt files in this directory.
DOCS_DIR = "T://GENAI_projects//RAG//Documents"

