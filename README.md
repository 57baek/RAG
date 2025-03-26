# 🧠 PubMed ChatBot: An AI-Powered Assistant for Evidence-Based Medical Research

> “I ain’t no physicist but I knows what matters.”  
> — *Popeye the Sailor*

---

## 📚 Overview

PubMed ChatBot is an interactive AI system designed to assist medical researchers, healthcare professionals, and students by retrieving and synthesizing scientific information directly from the PubMed database.

In a world overwhelmed by information, the challenge is not ignorance — it's excess. This project helps filter out noise and provides precise, research-backed answers to medical queries using a powerful Retrieval-Augmented Generation (RAG) pipeline and state-of-the-art language models.

---

## 🚀 Features

- 🔎 Vector-based semantic search over **PubMed abstracts**
- 📄 Retrieval of **full-text papers** using PubMed API
- 🧠 Generative answers powered by **LLMs** like GPT or local Ollama models
- 🧪 Supports both **OpenAI** and **local embedding** engines (e.g., `nomic-embed-text`)
- 📦 Local vector store with **ChromaDB**
- 💬 CLI-based **interactive querying system**
- 🧠 Optional **feedback memory system** for reinforcement and continuous improvement

---

## 🛠️ Project Structure

```
📁 rag-tutorial/
├── chroma/                       # Local vector DB storage
├── data/                         # Raw documents (PDFs, Markdown, etc.)
├── utils/                        # Helper modules
├── .env                          # API keys and credentials
├── requirements.txt              # All dependencies
├── get_embedding_function.py     # Configurable embedding function
├── populate_database.py          # Loads documents, chunks them, and populates ChromaDB
├── query_data.py                 # Accepts user queries and returns generated answers
```

---

## 🧪 System Workflow

### 1. Preprocessing & Indexing
- Downloads **PubMed abstracts** (via HPC or API)
- Embeds them using a selected embedding model
- Stores vectors in a **ChromaDB** vector store

### 2. Query & Retrieval
- User submits a question via CLI
- Query is embedded and matched using **cosine similarity**
- Top-K most relevant abstracts are retrieved

### 3. Fetch Full-Text Papers
- Extracts DOIs from abstracts
- Fetches full papers using **PubMed API**
- These papers become the context for the answer

### 4. Answer Generation
- Uses an LLM (e.g., GPT-3.5, GPT-4, DeepSeek, LLaMA) to answer based on:
  - 📄 Context = Retrieved Papers  
  - ❓ Question = User Query

---

## 🧠 Reinforcement Feedback System

- Users can pass `--feedback` flag during querying to indicate feedback.
- The system stores feedback in a dedicated **feedback memory database**.
- Every time a query is processed, the feedback is added to the prompt
  - 💬 The generated answer **reflects all previous user feedback**
- This feedback can be used in future sessions to:
  - Reinforce good answers
  - Avoid repeating mistakes
  - Enhance personalization of responses

---

## 🔍 Embedding Options

| Option                  | Description                              |
|-------------------------|------------------------------------------|
| `text-embedding-ada-002`| High-quality embedding via OpenAI API    |
| `nomic-embed-text`      | Local embedding via Ollama (no API needed)|

---

## 🖥️ Setup Instructions

1. **Install dependencies:**

```bash
pip install -r requirements.txt
pip install "unstructured[md]"  # If using Markdown loaders
```

2. **Create `.env` file if not using local LLM models:**

```
OPENAI_API_KEY=your-openai-key-here
```

3. **Populate ChromaDB:**

```bash
python3 populate_database.py --reset
```

4. **Query the chatbot:**

```bash
python3 query_data.py "What is the role of aspirin in heart disease?"
```

---

## 🧾 Chunking Strategy

- For long research papers, chunk by **sections** (e.g., Abstract, Introduction, Methods).
- For abstracts, chunking may not be needed or only light paragraph-based chunking.
- To handle multi-column PDFs or complex layouts:
  - Use `pdfplumber` or `pdfminer.six` for better parsing.

---

## 🧠 Future Improvements

- Hybrid retrieval (BM25 + vector search)
- UI for interactive querying
- Summarization of multi-document sets
- Fine-tuning for domain-specific behavior

---

## 🔐 License

This project is open to everyone!
Feel free to use, edit, copy, paste, share, or even taste it — seriously, go wild! 🍽️

Still, Always Be Civil!

---

## 🙏 Acknowledgements

- Prof. Mark Turner at Case Western Reserve University
- Case Western Reserve University HPC
- Pixegami (https://github.com/pixegami)
- PubMed
- OpenAI
- Ollama
- LangChain
- ChromaDB