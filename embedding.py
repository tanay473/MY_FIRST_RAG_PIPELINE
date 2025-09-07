# -*- coding: utf-8 -*-
"""
Handles the loading of the sentence embedding model.
"""
from sentence_transformers import SentenceTransformer
import config

def get_embedding_model():
    """Loads and returns the SentenceTransformer model."""
    print(f"Loading embedding model: {config.EMBEDDING_MODEL}...")
    model = SentenceTransformer(config.EMBEDDING_MODEL)
    print("Embedding model loaded.")
    return model
