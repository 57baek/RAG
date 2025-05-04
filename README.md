# 🧠 Medical RAG Chatbot

> “Information is not knowledge.”  
> — *Albert Einstein*

---

## 📘 Overview

**Medical RAG Chatbot** is a command-line assistant that answers evidence-based medical questions using real research papers from PubMed.  
It performs **Retrieval-Augmented Generation (RAG)** by combining:
- A dynamic PubMed fetcher 🧪
- Local vector database (Chroma) 📦
- Language models (LLMs) 🧠
- User feedback reinforcement 💬

All answers are **strictly grounded** in retrieved XML full-texts, making it ideal for **clinicians**, **researchers**, and **medical students** who demand **trustworthy**, **evidence-based** responses.

---

## 🗂️ Project Structure

```
medical-rag-chatbot/
│
├── app/                            # 📦 Main application
│   ├── cli/                        # 🖥️ CLI entrypoint
│   │   ├── cli.py
│   ├── configs/                    # ⚙️ Environment configs, prompts
│   │   ├── load_api.py
│   │   ├── load_db.py
│   │   ├── parameters.py
│   │   ├── paths.py
│   │   ├── prompts.py
│   ├── core/                       # 🔁 Core logic (RAG + Fetching)
│   │   ├── preprocessing.py
│   │   ├── pubmed_fetcher.py
│   │   ├── rag.py
│   ├── models/                     # 🤖 Model accessors
│   │   ├── chatting_model.py
│   │   ├── embedding_model.py
│   └── services/                   # 🔧 Utilities: Reset, Update, Loader
│       ├── auto_update.py
│       ├── feedback.py
│       ├── reset_database.py
│       ├── XMLDirectoryLoader.py
│
├── chroma/                         # 📦 Chroma vectorstore (generated)
├── data/                           # 📄 XML full-text downloads from PubMed
├── feedback/                       # 💬 User feedback storage (generated)
├── fileindex/                      # 📑 File index for update tracking (generated)
├── main.py                         # 🚀 CLI Runner
├── README.md                       # 📘 Project Documentation
├── requirements.txt                # 📦 Python Dependencies
└── .env                            # 🔐 Environment variables (private)
```

---

## 🚀 Features

- 🔎 Retrieve recent full-text research papers (PubMed → XML)
- 🧠 Answer questions using RAG powered by ChatGPT
- 📂 Automatically vectorize and index newly fetched papers
- 💬 Store and reuse user feedback to refine responses
- 🧹 Reset databases flexibly (data, embedding, feedback, file index)
- 🛡️ Safe retrieval: only use **open-access PMC** papers

---

## 📦 Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Set up environment variables

Create a `.env` file:

```bash
touch .env
```

Fill it like this:

```env
OPENAI_API_KEY=your-openai-key-here
NCBI_EMAIL=your-email@example.com
NCBI_API_KEY=your-ncbi-api-key-optional
```

⚠️ NCBI **requires** a valid email even if you don't use an API key.

---

## 💡 Usage

### Query and Download Papers:

```bash
python3 main.py query "How is EEG technology used in the development of brain-computer interfaces, and what are the latest advancements in decoding neural signals for BCI control?"
```

✅ This rewrites your natural language question into a PubMed search, fetches the most relevant papers, and downloads their **full-text XMLs** into the `data/` directory.

❗ **Important:**  
Once you load a query, all future "ask" commands will use **only the papers** fetched for that query.  
If you perform another query, all previously downloaded papers and associated data will be **automatically deleted** and replaced with the new set.

---

### Ask a question against local papers:

```bash
python3 main.py ask "What are EEG signal processing methods used for BCI?"
```

✅ This will vectorize your XMLs (if needed) and RAG-generate a trusted answer.

---

### Submit Feedback

```bash
python3 main.py feedback "Use bullet points and emojis for better clarity."
```

✅ This feedback will be automatically incorporated into all future generated answers to adjust their tone, formatting, or focus based on your preference!

---

### Reset Databases:

```bash
python3 main.py reset --all          # Reset everything
python3 main.py reset --db           # Reset downloaded XMLs
python3 main.py reset --em           # Reset Chroma vector DB
python3 main.py reset --fb           # Reset feedback database
python3 main.py reset --fi           # Reset file indexing
```

---

## 🧠 Feedback System

- 📂 Stores feedback inside `feedback/feedback.json`
- 🔁 Feedback is **inserted into every RAG prompt**
- 🔥 Helps models personalize tone, structure, and focus over time
- 🚀 Instant reinforcement without retraining the model

---

## 🧾 Prompt Template

### 🔎 Query Rewriting Prompt

```python
REWRITE_QUERY_FOR_PUBMED_SEARCH = """

You are an expert assistant specializing in PubMed searches.

Given a user's natural-language medical research question:

- Extract the most important **medical keywords** and **concepts** (diseases, techniques, body parts, etc.).
- Transform them into a **precise PubMed search query** that retrieves **highly relevant**, **recent** studies.
- Focus especially on **diagnostic techniques** (like EEG, SEEG) if they are mentioned.
- Make sure the search query remains **very specific** and **focused**.
- If appropriate, prefer studies from the **last 5-10 years** by adding date filters.
- Only output the rewritten search string — no explanation or extra commentary.

"""
```

---

### 💬 Answer Generation Prompt

```python
PROMPT_TEMPLATE = """

You are a professional AI assistant trained to answer complex scientific questions with a high degree of precision and clarity. Your task is to provide responses based **solely on the provided context**, which consists of excerpts from peer-reviewed scientific papers.

You are operating in the **medical and biomedical research domain**, where **accuracy, evidence-based reasoning, and cautious interpretation** are critical. You must **not guess, speculate, or hallucinate** any facts that are not explicitly present in the context.

If the context does **not contain enough information** to confidently address a part of the question, you must **clearly state that the information is insufficient**, or respond with **“I don’t know based on the provided context.”**

Do **not generate new knowledge** or provide personal opinions. Your role is strictly to **extract, summarize, and synthesize information that is directly supported by the context** you are given.

Incorporate the provided **user feedback** (if any) to improve tone, depth, or focus of your answer.

---

Context:
{context}

---

Feedback:
{feedback}

---

Question:
{question}

"""
```

---

✅ Now it's consistent, professional, and follows good README formatting.

Would you also like me to give you an even cooler bonus idea after this? (e.g., **auto-injecting the current year** for PubMed search prompts!) 🔥  
It could make your queries *always* prefer the most recent papers. 🚀

## 📌 Chunking Strategy

- **Splitter:** `RecursiveCharacterTextSplitter`
- **Settings:**
  - `chunk_size = 1000`
  - `chunk_overlap = 150`
- Each chunk gets a unique `source:page:index` ID.

✅ Ensures context granularity and optimal retrieval.

---

## 🧠 Future Enhancements

- 🔁 Hybrid retrieval (vector + keyword search)
- 🧪 Better automatic query rewriting using PubMed Mesh terms
- 🧬 Domain-specific fine-tuned LLM models
- 🌐 Web-based interface for live demo
- 🖼️ Multi-modal support (PDF figures, charts)

---

## 🔐 License

This project is fully open for academic, research, and educational purposes.  
Please feel free to **use, edit, remix, or extend**! 🎨🚀👩‍🎨

**Always remember the ABC: Always Be Civil!**

---

## 🙏 Acknowledgements

- Prof. Mark Turner at Case Western Reserve University (CWRU)
- Case Western Reserve University HPC Resources
- Pixegami GitHub Resources
- PubMed 
- NCBI
- OpenAI
- Ollama
- LangChain
- ChromaDB