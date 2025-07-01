# RBAC Chatbot: Retrieval-Augmented Generation with Role-Based Access Control

A Retrieval-Augmented Generation (RAG) based internal chatbot for enterprise use, featuring robust Role-Based Access Control (RBAC). Built with FastAPI, Qdrant vector database, Google Gemini API, and a modular, extensible architecture.

---

# Project Documentation

## Features
- **Role-Based Access Control (RBAC):** Restricts document access and chatbot responses based on user roles (engineering, finance, hr, marketing, general, c-level).
- **Retrieval-Augmented Generation (RAG):** Combines semantic search (Qdrant + Sentence Transformers) with Google Gemini for context-aware, accurate answers.
- **Document Indexing:** Supports Markdown and CSV files, chunked and embedded for efficient retrieval.
- **Admin Endpoints:** For indexing, stats, and user management.
- **Authentication:** HTTP Basic Auth (can be extended to OAuth/JWT).
- **Dockerized:** Easy deployment with Docker Compose (FastAPI, Qdrant, SQLite).

---

## Architecture

**Overview:**

- **FastAPI**: Main API server, handles auth, chat, admin, and indexing endpoints.
- **Qdrant**: Vector database for semantic search.
- **Sentence Transformers**: Generates embeddings for document chunks.
- **Google Gemini**: Generates final answers using retrieved context.
- **SQLite**: Stores user data and roles.
- **Resources/data**: Folder structure for role-based documents.

---

## Data Structure

- `resources/data/<role>/` — Documents for each role (e.g., engineering, finance, hr, marketing, general)
    - Markdown: `*.md`
    - CSV: `*.csv`

**Example:**
```
resources/data/engineering/engineering_master_doc.md
resources/data/hr/hr_data.csv
resources/data/general/employee_handbook.md
resources/data/marketing/marketing_report_2024.md
resources/data/finance/financial_summary.md
```

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-fork-url>
cd rbac-rag
```

### 2. Environment Variables
Create a `.env` file in the root with your Google Gemini API key:
```
GOOGLE_GENAI_API_KEY=your-gemini-api-key
```

### 3. Install Dependencies (Locally)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run with Docker Compose (Recommended)
```bash
docker-compose up --build
```
- FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Qdrant: [http://localhost:6333](http://localhost:6333)

---

## Usage

### 1. Index Documents (Admin Only)
- **Initialize Qdrant:**
  `POST /admin/index/init`
- **Index All Documents:**
  `POST /admin/index/documents`
- **Get Stats:**
  `GET /admin/index/stats`
- **Clear Index:**
  `DELETE /admin/index/clear`

### 2. User Authentication
- HTTP Basic Auth (username/password)
- Users and roles are stored in SQLite (`app/db/models.py`)

### 3. Chat Endpoint
- `POST /chat` (requires login)
- Body: `{ "message": "your question" }`
- Returns: RAG-powered answer, role-aware, with references

### 4. User Management (Admin Only)
- `GET /admin/users` — List users
- `POST /admin/users` — Add user
- `DELETE /admin/users/{username}` — Remove user

---

## Roles Provided
- **engineering**
- **finance**
- **general**
- **hr**
- **marketing**
- **c-level** (access to all docs)

---

## Extending & Customizing
- **Add new roles:** Create a new folder in `resources/data/` and update user roles in the DB.
- **Add new document types:** Extend `app/utils/file_loader.py`.
- **Change embedding model:** Update `EMBEDDING_MODEL` in `app/services/vector_store.py`.
- **Switch LLM:** Update the model in `app/services/rag_engine.py`.

---

## Dependencies
- fastapi
- uvicorn
- qdrant-client
- sentence-transformers
- pandas
- python-dotenv
- streamlit
- httpx
- google-genai
- markdown
- sqlalchemy

---

## License

This project is for academic and internal demonstration purposes.

---

## Credits
- Qdrant, Google Gemini, FastAPI, Sentence Transformers