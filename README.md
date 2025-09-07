# RAG Pipeline with Local LLM and Milvus

This project implements a Retrieval-Augmented Generation (RAG) pipeline that uses a local Large Language Model (LLM) hosted with LM Studio and a Milvus vector database for efficient document retrieval. The pipeline can process PDF and TXT documents, answer questions about their content, and is designed for easy setup and use.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Features

- **Local LLM Integration**: Connects to a local LLM (e.g., Llama) served via [LM Studio](https://lmstudio.ai/).
- **Vector-Based Retrieval**: Uses [Milvus](https://milvus.io/) (or Zilliz Cloud) for storing and searching document embeddings.
- **Multi-Format Document Support**: Ingests both `.pdf` and `.txt` files.
- **Automatic Re-ingestion**: Automatically re-processes and updates the vector database with the latest document versions on startup.
- **Easy to Use**: Simple command-line interface for asking questions.

## Project Structure

```
.
├── .env
├── .gitignore
├── config.py
├── document_loader.py
├── embedding.py
├── generator.py
├── ingestion.py
├── main.py
├── milvus_client.py
├── retriever.py
└── Documents/
    └── your_document.pdf
```

- **`main.py`**: The main script that orchestrates the entire RAG pipeline.
- **`config.py`**: Manages all configurations, loading sensitive data from a `.env` file.
- **`document_loader.py`**: Loads and splits documents from the `Documents` directory into manageable chunks.
- **`embedding.py`**: Handles the loading of the sentence-embedding model.
- **`ingestion.py`**: Manages the process of embedding document chunks and storing them in Milvus.
- **`milvus_client.py`**: A client for interacting with the Milvus vector database.
- **`retriever.py`**: Searches the Milvus database to find documents relevant to a user's query.
- **`generator.py`**: Generates a final answer using the local LLM and the retrieved documents.
- **`Documents/`**: The directory where you should place your `.pdf` and `.txt` files.

## How It Works

1.  **Document Loading & Chunking**: The pipeline reads all `.pdf` and `.txt` files from the `Documents` directory, extracts the text, and splits it into smaller, overlapping chunks.
2.  **Embedding & Ingestion**: Each chunk is converted into a vector embedding using a sentence-transformer model. These embeddings are then stored in a Milvus collection for fast similarity searches.
3.  **Retrieval**: When you ask a question, your query is also converted into an embedding. The retriever then searches the Milvus database to find the document chunks with the most similar embeddings.
4.  **Generation**: The retrieved chunks (the "context") and your original query are passed to the local LLM, which generates a final, context-aware answer.

## Getting Started

### Prerequisites

- Python 3.7+
- [LM Studio](https://lmstudio.ai/) installed and running with a downloaded model.
- A running [Milvus](https://milvus.io/docs/install_standalone-docker.md) instance (or a [Zilliz Cloud](https://zilliz.com/cloud) account).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is not provided in the current project structure, but it would be the standard way to manage dependencies.)*

3.  **Set up your environment variables:**
    Create a `.env` file in the root of the project and add the following, replacing the placeholder values with your own:

    ```env
    # --- Zilliz Cloud (Milvus) Configuration ---
    ZILLIZ_URI="YOUR_ZILLIZ_CLOUD_URI"
    ZILLIZ_TOKEN="YOUR_ZILLIZ_CLOUD_TOKEN"
    COLLECTION_NAME="my_documents"
    EMBEDDING_DIM=768 # Dimension of the embedding model (e.g., 768 for all-mpnet-base-v2)

    # --- Embedding Model Configuration ---
    EMBEDDING_MODEL='all-mpnet-base-v2'

    # --- LM Studio Configuration ---
    LM_STUDIO_BASE_URL="http://localhost:1234/v1"
    ```

## Usage

1.  **Add your documents**: Place the `.pdf` and `.txt` files you want to query into the `Documents` directory.

2.  **Run the pipeline**:
    ```bash
    python main.py
    ```

3.  **Ask questions**: Once the pipeline is running, you can enter your queries in the command line. Type `exit` to quit.

## Configuration

You can customize the pipeline's behavior by editing the `config.py` file or the `.env` file:

- **`COLLECTION_NAME`**: The name of the collection in Milvus where documents will be stored.
- **`EMBEDDING_MODEL`**: The sentence-transformer model to use for embeddings.
- **`LM_STUDIO_BASE_URL`**: The URL of your running LM Studio server.
- **`DOCS_DIR`**: The directory where the pipeline looks for documents.
