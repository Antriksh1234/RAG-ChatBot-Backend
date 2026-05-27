# Pandu Workspace - A RAG Chatbot 🐼

A conversational RAG (Retrieval-Augmented Generation) knowledge workspace built using FastAPI, PostgreSQL + pgvector, Next.js, and modern LLM orchestration techniques.

Pandu Workspace allows users to create a knowledge base, ask conversational questions over documents, and receive grounded AI-generated responses with source attribution and streaming support.

---

# ✨ Features

- Conversational RAG pipeline
- Semantic vector search using pgvector
- Hybrid retrieval with keyword reranking
- Conversational query rewriting
- Streaming AI responses
- Source-grounded answers
- Conversational memory optimization
- Editable knowledge base
- Modern streaming chat UI
- Auto-scroll chat experience
- Dark themed responsive interface

---

# 🧠 Core RAG Concepts Implemented

This project focuses heavily on understanding and implementing core RAG engineering concepts instead of only building a simple chatbot UI.

Implemented concepts include:

- Embedding generation
- Vector similarity search
- Chunking strategies
- Hybrid retrieval
- Retrieval reranking
- Query rewriting
- Conversational memory optimization
- Streaming architecture
- Source attribution
- Retrieval debugging & observability

---

# ⚙️ Tech Stack

## Backend
- FastAPI
- PostgreSQL
- pgvector
- SQLAlchemy
- Sentence Transformers
- Groq API

## Frontend
- Next.js
- React
- Tailwind CSS

## LLM / AI
- Llama 3.3 70B (Groq)
- Sentence Transformers Embeddings

---

# 🗄️ PostgreSQL + pgvector Setup

This project uses PostgreSQL with the `pgvector` extension for vector similarity search.

You can run PostgreSQL in multiple ways:

- Local PostgreSQL installation
- Docker
- Hosted PostgreSQL providers (Neon, Supabase, Railway, etc.)

---

## Enable pgvector Extension

Run the following SQL:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## Example Database URL

```env
DATABASE_URL=postgresql://username:password@localhost:5432/pandu_workspace
```

---

# 🏗️ Architecture



![Pandu Workspace Architecture](./rag_chatbot.png)

---

# 🔄 Flow

```text
User Query
    ↓
Query Rewriting
    ↓
Embedding Generation
    ↓
Vector Similarity Search
    ↓
Hybrid Keyword Reranking
    ↓
Context Assembly
    ↓
LLM Response Streaming
    ↓
Source Attribution
```

---

# 🔍 Retrieval Pipeline

## 1. Query Rewriting

Conversational questions are rewritten into standalone queries using previous chat history and conversational context.

Example:

```text
"What about his favorite food?"
↓
"What is Pandu's favorite food?"
```

This significantly improves retrieval quality in conversational flows.

---

## 2. Vector Search

The rewritten query is embedded and matched against document chunk embeddings stored in PostgreSQL using pgvector cosine similarity search.

---

## 3. Hybrid Reranking

Retrieved chunks are reranked using lightweight keyword overlap scoring on top of semantic similarity.

This helps improve retrieval precision for keyword-heavy queries.

---

## 4. Context Assembly

Top ranked chunks are combined into contextual information for the LLM.

---

## 5. Streaming Responses

Responses are streamed token-by-token from the backend to provide real-time AI chat experience.

---

## 6. Source Attribution

Retrieved documents are attached to responses so users can verify answers and navigate to original documents.

---

# 🧠 Conversational Memory Optimization

To avoid infinite token growth:

- Older conversations are summarized
- Recent messages are retained
- Query rewriting uses:
  - summarized memory
  - recent conversational history

This helps maintain conversational continuity while keeping prompts efficient.

---

# 📡 Streaming Architecture

The application uses streaming responses from the backend to create a responsive AI chat experience.

Currently:
- answer tokens stream live
- document sources are returned via HTTP headers

Future improvements may include full SSE (Server-Sent Events) architecture.

---

# 🖥️ UI Features

- Fixed navbar layout
- Auto-scrolling chat
- Streaming assistant responses
- Source pills with document linking
- Responsive dark UI
- Panda branding 😄

---

# 🚀 Running Locally

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

# 📌 Future Improvements

- Full SSE event streaming
- Citation-level chunk highlighting
- PDF/DOCX ingestion
- Persistent conversational sessions
- Advanced reranker models
- Metadata filtering
- Multi-user workspace support
- Retrieval evaluation framework

---

# 📚 What I Learned

This project helped me deeply understand:

- how conversational RAG systems work
- retrieval quality challenges
- memory management in AI systems
- streaming architectures
- grounding AI responses with sources
- balancing semantic search with keyword retrieval
- frontend/backend orchestration for AI applications

---

# 🐼 Pandu AI

Built as a learning-focused conversational AI workspace project to explore modern RAG system design and conversational AI engineering.