# 🚀 Modular RAG Pipeline with Milvus & LM Studio
## 📝 Overview
This project implements a complete, modular Retrieval-Augmented Generation (RAG) pipeline in Python. It is designed to answer user queries based on a custom knowledge base of documents by leveraging a local Large Language Model (LLM). The system uses Zilliz Cloud (a managed Milvus service) for efficient, scalable vector search and integrates with any LLM served through LM Studio.

## ✨ Key Features
`🧱 Modular Architecture`: The codebase is organized into distinct, single-responsibility modules, making it easy to maintain, extend, and debug.

`📄 Multi-Format Document Support`: Ingest and process information from multiple file types, including .pdf and .txt documents.

`🔍 Scalable Vector Search`: Utilizes Zilliz Cloud for robust and high-performance similarity searches using an HNSW index.

`💻 Local LLM Integration`: Connects seamlessly with any local LLM served via LM Studio, ensuring data privacy and cost-free generation.

`⚡ Efficient Data Ingestion`: Implements batch processing and a tqdm progress bar for speedy and transparent ingestion of large document sets.

`🧩 Robust Document Chunking`: Employs a character-based splitting strategy to handle large documents and avoid database field limits.

`⌨️ Interactive CLI`: Provides a user-friendly command-line interface for asking questions and receiving answers.

## 🛠️ Technology Stack
`Orchestration`: Python 🐍

`Vector Database`: Milvus (via Zilliz Cloud) ☁️

`LLM Serving`: LM Studio 🧠

`Embedding Model`: Sentence-Transformers

## Core Libraries:

`pymilvus`: For database interaction.

`sentence-transformers`: For vector embeddings.

`openai`: For API communication with LM Studio.

`PyMuPDF`: For PDF text extraction.

`tqdm`: For progress bars.

`python-dotenv`: For environment variable management.

## ⚙️ How It Works
`📥 Load & Chunk`: The pipeline scans a documents directory, extracts text from all .pdf and .txt files, and splits the content into small, overlapping chunks.

`✒️ Embed & Ingest`: Each text chunk is converted into a vector embedding. These embeddings are then inserted in batches into the Milvus collection on Zilliz Cloud.

`🔎 Query & Retrieve`: A user's query is converted into an embedding and used to search Milvus for the most similar document chunks.

`🧠 Augment & Generate`: The retrieved text chunks are combined with the original query into a prompt, which is sent to the local LLM.

`💬 Respond`: The LLM generates an answer based on the provided context, which is then displayed to the user.

## 🔧 Setup & Running
For detailed setup and execution instructions, please refer to the main project documentation. The basic steps involve:

Starting Zilliz Cloud and LM Studio.

Setting up the Python environment and installing dependencies from requirements.txt.

Configuring your credentials in a .env file.

Placing your .pdf and .txt files in the documents directory.

Running the main script with python main.py.
