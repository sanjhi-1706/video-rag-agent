# AI Video Summarizer & Chat (Multimodal RAG System)

An end-to-end AI system that transforms YouTube videos into structured, searchable knowledge using Retrieval-Augmented Generation (RAG). The system enables users to query video content, generate summaries, and extract insights without watching the full video.

---

## Features

* Chat with video using context-aware question answering
* Hybrid retrieval using FAISS (semantic search) and BM25 (keyword search) with cross-encoder re-ranking
* Asynchronous processing using Redis and RQ for handling long-running tasks
* Speech-to-text transcription using Whisper (local inference)
* Multimodal support using BLIP for visual captioning
* Query-based summarization (beginner, exam-focused, bullet points, detailed)
* Interactive frontend using Streamlit

---

## System Architecture

The system follows a modular pipeline combining asynchronous processing and retrieval-based generation.

### High-Level Flow

User Input (UI)
↓
Streamlit Frontend
↓
Redis Queue
↓
Worker (RQ)
↓
Video Processing Pipeline
↓
RAG System
↓
LLM Response (Groq)

---

## Detailed Pipeline

### Step 1: Video Input

* User provides a YouTube URL through the Streamlit interface
* The request is pushed to a Redis queue

### Step 2: Asynchronous Processing

* RQ worker picks up the job
* Ensures the UI remains responsive

### Step 3: Audio Extraction

* YouTube video is processed using a downloader
* Audio is extracted and stored locally

### Step 4: Transcription

* Whisper model converts audio into text
* Transcript is stored for further processing

### Step 5: (Optional) Visual Processing

* Frames are extracted from video
* BLIP generates captions
* Visual context is merged with transcript

### Step 6: Text Processing

* Transcript is split into chunks
* Each chunk is converted into embeddings

### Step 7: Hybrid Retrieval

* FAISS retrieves semantically relevant chunks
* BM25 retrieves keyword-matching chunks
* Cross-encoder re-ranks results

### Step 8: Query Handling

* User query is classified:

  * General → full context used
  * Specific → retrieved chunks used

### Step 9: Response Generation

* Context is passed to LLM (Groq API)
* Answer or summary is generated

---

## Folder Structure

```plaintext
video-rag-agent/
│
├── app/
│   ├── services/
│   │   ├── youtube_service.py        # Download video/audio
│   │   ├── stt_service.py            # Whisper transcription
│   │   ├── embedding_service.py      # Generate embeddings
│   │   ├── retriever.py              # Hybrid retrieval (FAISS + BM25)
│   │   ├── reranker_service.py       # Cross-encoder ranking
│   │   ├── qa_service.py             # LLM response generation
│   │   ├── summary_service.py        # Query-based summarization
│   │   ├── blip_service.py           # Image captioning (optional)
│   │
│   ├── rag/
│   │   ├── chunking.py               # Text chunking logic
│   │   ├── bm25.py                   # BM25 implementation
│   │
│   ├── db/
│   │   ├── vector_db.py              # FAISS index handling
│   │
│   ├── workers/
│   │   ├── worker.py                 # RQ worker setup
│   │   ├── tasks.py                  # Async processing pipeline
│
├── frontend/
│   ├── streamlit_app.py              # UI (input + chat + summary)
│
├── data/                             # Local storage (ignored in git)
│
├── test_chat.py                      # Local testing of RAG
├── test_async.py                     # Async job testing
├── check_job.py                      # Job status checker
├── requirements.txt
├── README.md
```

---

## Core Data Flow

### End-to-End Execution

YouTube URL
↓
Download Audio
↓
Whisper Transcription
↓
Chunking
↓
Embeddings
↓
FAISS Index + BM25
↓
Query
↓
Hybrid Retrieval
↓
Re-ranking
↓
LLM (Groq)
↓
Final Answer

---

## Query Processing Flow

User Query
↓
Query Type Detection
↓
┌───────────────┬────────────────┐
│ General Query │ Specific Query │
└──────┬────────┴───────┬────────┘
↓                ↓
Full Transcript     Hybrid Retrieval
↓                ↓
└──────→ Context Selection
↓
LLM Response

---

## Installation

```bash
git clone https://github.com/<your-username>/video-rag-agent.git
cd video-rag-agent

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Running the System

### Start Redis

```bash
brew services start redis
```

### Start Worker

```bash
export PYTHONPATH=.
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python app/workers/worker.py
```

### Start UI

```bash
export PYTHONPATH=.
streamlit run frontend/streamlit_app.py
```

---

## Limitations

* Currently supports English transcription only
* Visual understanding is basic (frame-level captions)
* Not optimized for very long videos

---

## Future Improvements

* Multi-language support
* Better multimodal alignment (timestamp-based fusion)
* Deployment using Docker and cloud services
* Persistent vector database

---

## Author

Sanjhi Parikh
