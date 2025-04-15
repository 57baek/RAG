# 🧠 Medical RAG Chatbot

> “Information is not knowledge.”  
> — *Albert Einstein*

---

## 📘 Overview

**Medical RAG Chatbot** is a command-line assistant designed to answer evidence-based medical questions using scientific papers (e.g., PubMed). It leverages **Retrieval-Augmented Generation (RAG)** and integrates vector databases, LLMs (like GPT or Ollama), and user feedback for enhanced precision and trustworthiness.

All responses are grounded strictly in retrieved scientific content — ideal for clinicians, researchers, or medical students.

---

## 🗂️ Project Structure

```
medical-rag-chatbot/
│
├── app/                            # 📦 Main application module
│   ├── cli/                        # 🖥️ CLI entrypoint
│   │   ├── __init__.py
│   │   └── cli.py
│   ├── configs/                    # ⚙️ Paths, prompts, and key management
│   │   ├── __init__.py
│   │   ├── load_api_key.py
│   │   ├── paths.py
│   │   └── prompts.py
│   ├── core/                       # 🔁 Core logic: RAG + vectorization
│   │   ├── __init__.py
│   │   ├── rag.py
│   │   └── vectorization.py
│   ├── models/                     # 🤖 LLM and embedding model wrappers
│   │   ├── __init__.py
│   │   ├── chatting_model.py
│   │   └── embedding_model.py
│   └── services/                   # 🔧 Feedback, auto-update, and resets
│       ├── __init__.py
│       ├── auto_update.py
│       ├── feedback.py
│       └── reset.py
│
├── data/                           # 📄 Folder to store PDF documents
├── docs/                           # 📚 Optional documentation
├── tests/                          # ✅ Unit and integration tests
├── .env.template                   # 🔐 Template for environment variables
├── .gitignore                      # 🚫 Git exclusions
├── main.py                         # 🚀 App entrypoint (runs the CLI)
├── README.md                       # 📘 Project documentation
└── requirements.txt                # 📦 Python dependencies
```

---

## 🚀 Features

- 🔍 Vector-based semantic search over local PDF documents
- 🧠 LLM-powered answers with grounded scientific context
- 💬 Feedback memory system to refine response behavior
- 📁 Auto-indexing of newly added or updated PDFs
- 🧪 Supports both OpenAI and local embedding/LLM engines
- 🧹 Flexible database reset via CLI flags

---

## 📦 Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Optional (for markdown or unstructured content):

```bash
pip install "unstructured[md]"
```

---

### 2. Environment Setup

Copy the environment template and add your API keys:

```bash
cp .env.template .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your-key-here
```

---

## 💡 Usage

### Ask a question:

```bash
python3 main.py ask "What is the role of dopamine in Parkinson's?"
```

### Add user feedback:

```bash
python3 main.py feedback "Explain each finding more clearly and use numbered lists."
```

### Reset databases:

```bash
python3 main.py reset --all         # Full reset
python3 main.py reset --em          # Reset embedding DB
python3 main.py reset --fb          # Reset feedback DB
python3 main.py reset --fi          # Reset file index
```

---

## 🧠 Feedback System

- Feedback is stored in `feedback/feedback.json`.
- Every RAG prompt includes all historical feedback.
- Reinforces helpful patterns and filters unwanted ones over time.

---

## 🧾 Prompt Template

The system uses a carefully formatted instruction template to ensure precise, grounded outputs:

```
You are a professional AI assistant answering scientific questions based strictly on provided content. 
You are dealing with medical questions where precision matters the most. 
All answers must be strictly based on the given scientific excerpts. 
You must not generate opinions or make assumptions. 
If the context lacks sufficient detail, respond with "I don't know" or a request for more information.

---

Context:
{context}

---

Feedback:
{feedback}

---

Question:
{question}
```

---

## 📌 Chunking Strategy

- Uses `RecursiveCharacterTextSplitter`
- Parameters:
  - `chunk_size = 1000`
  - `chunk_overlap = 150`
- Each chunk is assigned a unique ID: `source:page:index`

---

## 🧠 Future Enhancements

- 🔁 Hybrid retrieval (BM25 + vector search)
- 🌐 Web interface
- 📄 Summarization of multi-document answers
- ⚗️ Domain-specific model fine-tuning
- 🧬 Multi-modal inputs (e.g., images, figures)

---

## 🔐 License

This project is open to everyone!
Feel free to use, edit, copy, paste, share, or even taste it — seriously, go wild! 🍽️

Still, Always Be Civil (ABC)!

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