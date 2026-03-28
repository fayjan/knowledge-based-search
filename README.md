# Knowledge Based Search (KBS) 🔍

A professional **Retrieval-Augmented Generation (RAG)** system built for the Unthinkable Solutions technical assignment. This project enables users to upload multiple PDF documents and receive synthesized, succinct answers based strictly on the provided context.

## 🌟 Key Features
- **Decoupled Architecture:** Separate FastAPI backend and Streamlit frontend for scalability.
- **Advanced RAG Pipeline:** Implements **LangChain Expression Language (LCEL)** for a modular and efficient retrieval chain.
- **Deterministic Synthesis:** LLM temperature is set to `0` to ensure factual grounding and minimize hallucinations.
- **Smart Chunking:** Uses `RecursiveCharacterTextSplitter` to maintain context across document fragments.
- **Vectorized Search:** Persistent semantic search powered by **ChromaDB**.

## 🏗️ System Architecture
The application follows a standard RAG workflow:
1. **Ingestion:** PDF text extraction and recursive chunking.
2. **Embedding:** Text chunks are converted to vectors via OpenAI `text-embedding-3-small`.
3. **Retrieval:** Semantic similarity search to find the top $k$ relevant context blocks.
4. **Synthesis:** GPT-4o generates a succinct response using a custom-engineered prompt.



## 🛠️ Tech Stack
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Orchestration:** LangChain (LCEL)
- **LLM:** OpenAI GPT-4o (via API)
- **Vector Store:** ChromaDB
- **Environment:** Python 3.11+

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
    git clone [https://github.com/fayjan/knowledge-based-search](https://github.com/fayjan/knowledge-based-search)
    cd knowledge-based-search
```
### 2. Create a Virtual Environment
For Mac / Linux:
```bash
    python3 -m venv .venv
    source .venv/bin/activate
```

For Windows:
```bash
    python -m venv .venv
    .venv\Scripts\activate
```
### 3. Install Dependencies
```bash
    pip install -r requirements.txt
```

### 4. Configuration
Create a .env file in the root directory and add your OpenAI API key:
OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY

### 💻 Running the Application
```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    streamlit run frontend/app.py
```