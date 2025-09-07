# -*- coding: utf-8 -*-
"""
Handles loading documents from a directory and splitting them into chunks.
Supports both PDF and TXT files.
"""
import os
import fitz  # PyMuPDF

def chunk_text(text, chunk_size=1500, chunk_overlap=150):
    """
    Splits text into smaller chunks based on a character count, with overlap.
    This is a more robust method than splitting by paragraphs alone.
    """
    if not text:
        return []
        
    chunks = []
    start_index = 0
    while start_index < len(text):
        end_index = start_index + chunk_size
        chunks.append(text[start_index:end_index])
        start_index += chunk_size - chunk_overlap
    return chunks

def load_and_split_documents(directory_path):
    """
    Loads all .pdf and .txt files from a directory, extracts text,
    and splits them into chunks of a manageable size.
    
    Args:
        directory_path (str): The path to the directory containing the files.

    Returns:
        list[str]: A list of document chunks.
    """
    print(f"Loading documents from: {directory_path}")
    document_chunks = []
    
    if not os.path.exists(directory_path):
        print(f"Error: Directory not found at '{directory_path}'. Please create it.")
        return []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        content = ""
        try:
            if filename.lower().endswith(".pdf"):
                with fitz.open(file_path) as doc:
                    for page in doc:
                        content += page.get_text() # type: ignore
                print(f"  - Extracted text from PDF: '{filename}'")

            elif filename.lower().endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"  - Extracted text from TXT: '{filename}'")

            # Now, chunk the extracted content regardless of its source
            if content:
                # Use the new character-based chunking function
                chunks = chunk_text(content)
                # Clean the chunks
                cleaned_chunks = [chunk.strip().replace('\n', ' ') for chunk in chunks if chunk.strip()]
                document_chunks.extend(cleaned_chunks)
                print(f"    - Split into {len(cleaned_chunks)} chunks.")

        except Exception as e:
            print(f"  - Error processing {filename}: {e}")
                
    if not document_chunks:
        print("Warning: No documents were loaded. Make sure the 'documents' directory is not empty and contains valid .pdf or .txt files.")

    return document_chunks

