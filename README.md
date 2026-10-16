# AI Assistant

> 🚧 *Work in progress*

A conversational assistant built on a **LangChain agent** that uses **RAG** (*Retrieval-Augmented Generation*).
Before it answers, the agent can look up relevant information in a **PostgreSQL / pgvector** vector store.

---

## ✨ Features

- 🔎 **Semantic search** with HuggingFace embeddings (`sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions)
- 🗄️ **Vector storage** in PostgreSQL with the `pgvector` extension (via `langchain-postgres`)
- 🤖 **LangChain agent** that decides on its own when to call the `retrieve_context` tool
- 🔌 **Works with any LLM provider** that has an OpenAI-compatible API (OpenAI, OpenRouter, Ollama, vLLM, LM Studio…)
- ⚙️ **Configured through environment variables** (`.env`)

---

## 🏗️ Architecture

```text
┌──────────────┐     ┌────────────────────┐     ┌──────────────────────┐
│     User     │ ──▶ │  LangChain Agent   │ ──▶ │  LLM (OpenAI API)    │
└──────────────┘     └─────────┬──────────┘     └──────────────────────┘
                               │ tool: retrieve_context
                               ▼
                     ┌────────────────────┐     ┌──────────────────────┐
                     │     Retriever      │ ──▶ │ PostgreSQL + pgvector│
                     │  (HF embeddings)   │     │ collection Assistant │
                     └────────────────────┘     └──────────────────────┘
```

---

## 📁 Project Structure

```text
Assistant/
├── .venv/              # Virtual environment (virtualenv)
├── src/
│   ├── __init__.py
│   └── main.py         # Entry point: RAG and agent setup
└── README.md
```

---

## 📋 Requirements

- **Python 3.11+**
- **PostgreSQL** with the [`pgvector`](https://github.com/pgvector/pgvector) extension
- An API key for an OpenAI-compatible provider

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Assistant
```

### 2. Create and activate the virtual environment

```bash
virtualenv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install langchain langchain-core langchain-openai langchain-huggingface \
            langchain-postgres "psycopg[binary]" sentence-transformers python-dotenv
```

### 4. Set up the database

With Docker (the easiest way):

```bash
docker run -d --name pgvector \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=rag \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

Or, on an existing PostgreSQL instance:

```sql
CREATE DATABASE rag;
\c rag
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```dotenv
# --- Database ---
SQL_USER=postgres
SQL_PASS=postgres
SQL_ADDRESS=localhost

# --- LLM ---
MODEL_NAME=gpt-4o-mini
PROVIDER_URL=https://api.openai.com/v1
PROVIDER_KEY=sk-...
```

| Variable       | Description                                  | Example                     |
|----------------|----------------------------------------------|-----------------------------|
| `SQL_USER`     | PostgreSQL user                              | `postgres`                  |
| `SQL_PASS`     | PostgreSQL password                          | `postgres`                  |
| `SQL_ADDRESS`  | PostgreSQL server host (port `5432`)         | `localhost`                 |
| `MODEL_NAME`   | Name of the model to use                     | `gpt-4o-mini`               |
| `PROVIDER_URL` | Base URL of the OpenAI-compatible API        | `https://api.openai.com/v1` |
| `PROVIDER_KEY` | Provider API key                             | `sk-...`                    |

> ⚠️ Never commit your `.env` file. Add it to your `.gitignore`.

---

## 📥 Populating the Vector Store

The agent can only answer from documents stored in the `Assistant` collection.
Here's how to add documents:

```python
from langchain_core.documents import Document

docs = [
    Document(
        page_content="Lucachinou is a developer specialized in AI.",
        metadata={"source": "profile"},
    ),
]

vs.add_documents(docs)
```

---

## ▶️ Usage

```bash
python src/main.py
```

The script sends a question to the agent. The agent searches the vector store if it needs to, then prints the LLM's answer to the console.

---

## 🗺️ Roadmap

- [ ] Document ingestion script (PDF, Markdown, TXT…)
- [ ] Interactive chat interface (CLI or web)
- [ ] Conversation memory
- [ ] Unit tests

---

## 📄 License

The license used in this project is GNU GENERAL PUBLIC LICENSE v3.