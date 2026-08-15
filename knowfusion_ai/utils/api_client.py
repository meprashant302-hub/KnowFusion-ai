"""
api_client.py
--------------
THIS IS THE FILE THE BACKEND TEAM SHOULD EDIT.

Every function below is the single point of contact between the Streamlit
frontend and the backend/RAG service. Right now each function returns mock
data (see `utils/mock_data.py`) so the UI is fully demo-able without a
backend running.

HOW TO INTEGRATE A REAL BACKEND
--------------------------------
1. Set `USE_MOCK = False` at the bottom of this file (or read it from an
   environment variable / st.secrets — see `BACKEND_BASE_URL` below).
2. Implement the body of each function to call your real API
   (FastAPI / Flask / Node / whatever) using `requests`.
3. Keep the RETURN SHAPE of every function identical to what's documented
   in its docstring. As long as the shape doesn't change, no other file in
   this project (pages/*.py) needs to be touched.
4. Suggested backend stack: FastAPI + a vector DB (FAISS / Chroma / Pinecone)
   + an LLM provider. Auth can be JWT-based; see `utils/auth.py` for what
   the frontend currently expects from a login response.

All functions are intentionally synchronous and simple (no async) to match
Streamlit's execution model. Raise exceptions for hard failures — pages
already wrap calls in try/except and show `st.error(...)`.
"""

import os
import time
import random
from typing import List, Dict, Optional

from utils import mock_data

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# BACKEND TEAM: point this at your real API once it exists, e.g. via
# an environment variable or st.secrets["BACKEND_BASE_URL"].
BACKEND_BASE_URL = os.environ.get("KNOWFUSION_BACKEND_URL", "http://localhost:8000/api")

# Toggle this to False once real endpoints below are implemented.
USE_MOCK = True


# ---------------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------------
def login(username: str, password: str) -> Dict:
    """
    Authenticate a user.

    Expected REAL response shape (e.g. POST {BACKEND_BASE_URL}/auth/login):
        {
            "success": bool,
            "token": str | None,        # JWT or session token
            "user": {
                "id": str,
                "name": str,
                "email": str,
            } | None,
            "error": str | None,        # populated only if success == False
        }
    """
    if USE_MOCK:
        time.sleep(0.3)  # simulate network latency
        # DEMO CREDENTIALS (frontend-only): any non-empty username/password
        # combo works, OR use demo / demo123 explicitly.
        if username and password:
            return {
                "success": True,
                "token": "mock-token-123",
                "user": {
                    "id": "user_001",
                    "name": username.split("@")[0].capitalize() if username else "Prashant",
                    "email": username if "@" in username else f"{username}@example.com",
                },
                "error": None,
            }
        return {"success": False, "token": None, "user": None, "error": "Invalid credentials"}

    # TODO(backend): replace with e.g.
    # resp = requests.post(f"{BACKEND_BASE_URL}/auth/login",
    #                       json={"username": username, "password": password})
    # return resp.json()
    raise NotImplementedError("Wire this up to the real auth endpoint.")


def signup(name: str, email: str, password: str) -> Dict:
    """
    Register a new user.

    Expected REAL response shape (POST {BACKEND_BASE_URL}/auth/signup):
        {
            "success": bool,
            "token": str | None,
            "user": {"id": str, "name": str, "email": str} | None,
            "error": str | None,
        }
    """
    if USE_MOCK:
        time.sleep(0.3)
        if name and email and password:
            return {
                "success": True,
                "token": "mock-token-new-user",
                "user": {"id": "user_new", "name": name, "email": email},
                "error": None,
            }
        return {"success": False, "token": None, "user": None, "error": "All fields are required"}

    raise NotImplementedError("Wire this up to the real signup endpoint.")


# ---------------------------------------------------------------------------
# DOCUMENTS
# ---------------------------------------------------------------------------
def upload_document(file_bytes: bytes, filename: str) -> Dict:
    """
    Upload a document to the knowledge base for ingestion/embedding.

    Expected REAL response shape (POST {BACKEND_BASE_URL}/documents/upload):
        {
            "success": bool,
            "document": {
                "id": str,
                "name": str,
                "type": str,        # "pdf" | "docx" | "txt" ...
                "status": str,      # "processing" | "ready" | "failed"
            } | None,
            "error": str | None,
        }
    """
    if USE_MOCK:
        time.sleep(0.5)
        ext = filename.split(".")[-1].lower()
        return {
            "success": True,
            "document": {
                "id": f"src_{random.randint(100, 999)}",
                "name": filename,
                "type": ext,
                "status": "ready",
            },
            "error": None,
        }

    # TODO(backend): multipart file upload, e.g.
    # resp = requests.post(f"{BACKEND_BASE_URL}/documents/upload",
    #                       files={"file": (filename, file_bytes)})
    # return resp.json()
    raise NotImplementedError("Wire this up to the real upload endpoint.")


def list_sources() -> List[Dict]:
    """
    Fetch all documents currently in the user's knowledge base.

    Expected REAL response shape (GET {BACKEND_BASE_URL}/documents):
        [
            {
                "id": str,
                "name": str,
                "type": str,          # "pdf" | "docx" ...
                "location": str,      # e.g. "Page 12" or a URL
                "relevance": int,     # 0-100, only meaningful post-query
                "uploaded_at": str,   # ISO 8601
            },
            ...
        ]
    """
    if USE_MOCK:
        time.sleep(0.2)
        return mock_data.MOCK_SOURCES

    # TODO(backend): resp = requests.get(f"{BACKEND_BASE_URL}/documents")
    # return resp.json()
    raise NotImplementedError("Wire this up to the real documents endpoint.")


def compare_documents(document_ids: List[str]) -> Dict:
    """
    Ask the backend to compare 2+ documents.

    Expected REAL response shape (POST {BACKEND_BASE_URL}/documents/compare):
        {"comparison": str}   # markdown-formatted comparison text
    """
    if USE_MOCK:
        time.sleep(0.6)
        return {
            "comparison": (
                "**Mock comparison output.**\n\nOnce connected, this will show a "
                "structured, section-by-section comparison of the selected "
                "documents (similarities, differences, and key contrasting points)."
            )
        }
    raise NotImplementedError("Wire this up to the real compare endpoint.")


def summarize_document(document_id: str) -> Dict:
    """
    Ask the backend to summarize a single document.

    Expected REAL response shape (POST {BACKEND_BASE_URL}/documents/summarize):
        {"summary": str}
    """
    if USE_MOCK:
        time.sleep(0.5)
        return {
            "summary": (
                "**Mock summary.** Once connected, this will return an "
                "AI-generated summary of the selected document's key points, "
                "structured with headings and bullet points."
            )
        }
    raise NotImplementedError("Wire this up to the real summarize endpoint.")


def generate_quiz(document_id: str, num_questions: int = 5) -> Dict:
    """
    Ask the backend to generate a quiz from a document.

    Expected REAL response shape (POST {BACKEND_BASE_URL}/documents/quiz):
        {
            "questions": [
                {
                    "question": str,
                    "options": [str, str, str, str],
                    "correct_index": int,
                    "explanation": str,
                },
                ...
            ]
        }
    """
    if USE_MOCK:
        time.sleep(0.5)
        return {
            "questions": [
                {
                    "question": "What does RAG stand for?",
                    "options": [
                        "Retrieval-Augmented Generation",
                        "Random Access Generation",
                        "Rapid AI Growth",
                        "Retrieval And Grouping",
                    ],
                    "correct_index": 0,
                    "explanation": "RAG = Retrieval-Augmented Generation, combining retrieval with generation.",
                }
            ]
            * num_questions
        }
    raise NotImplementedError("Wire this up to the real quiz endpoint.")


def generate_mind_map(document_id: str) -> Dict:
    """
    Ask the backend to generate a mind-map graph structure from a document.

    Expected REAL response shape (POST {BACKEND_BASE_URL}/documents/mindmap):
        {
            "nodes": [{"id": str, "label": str}, ...],
            "edges": [{"source": str, "target": str, "label": str | None}, ...],
        }
    """
    if USE_MOCK:
        time.sleep(0.5)
        return {
            "nodes": [
                {"id": "n1", "label": "RAG"},
                {"id": "n2", "label": "Retriever"},
                {"id": "n3", "label": "Generator (LLM)"},
                {"id": "n4", "label": "Knowledge Base"},
            ],
            "edges": [
                {"source": "n1", "target": "n2", "label": "uses"},
                {"source": "n1", "target": "n3", "label": "uses"},
                {"source": "n2", "target": "n4", "label": "queries"},
            ],
        }
    raise NotImplementedError("Wire this up to the real mind-map endpoint.")


# ---------------------------------------------------------------------------
# CHAT
# ---------------------------------------------------------------------------
def send_chat_message(message: str, chat_id: Optional[str], history: List[Dict]) -> Dict:
    """
    Send a user chat message and get the assistant's RAG-grounded reply.

    Expected REAL response shape (POST {BACKEND_BASE_URL}/chat):
        {
            "reply": str,
            "sources_used": [str, ...],   # list of document IDs cited
            "has_web_info": bool,         # whether web augmentation was used
            "chat_id": str,               # session id (new or existing)
        }
    """
    if USE_MOCK:
        time.sleep(0.8)
        return {
            "reply": (
                f"(Mock response) You asked: \u201c{message}\u201d.\n\n"
                "Once the backend is connected, this will be a real answer "
                "generated from your uploaded documents using the RAG pipeline."
            ),
            "sources_used": [s["id"] for s in mock_data.MOCK_SOURCES[:2]],
            "has_web_info": False,
            "chat_id": chat_id or "chat_new_001",
        }

    # TODO(backend): resp = requests.post(f"{BACKEND_BASE_URL}/chat",
    #                       json={"message": message, "chat_id": chat_id, "history": history})
    # return resp.json()
    raise NotImplementedError("Wire this up to the real chat endpoint.")


def list_chat_sessions() -> List[Dict]:
    """
    Fetch the list of past chat sessions for the sidebar.

    Expected REAL response shape (GET {BACKEND_BASE_URL}/chats):
        [{"id": str, "title": str, "updated_at": str}, ...]
    """
    if USE_MOCK:
        time.sleep(0.2)
        return mock_data.MOCK_CHAT_SESSIONS
    raise NotImplementedError("Wire this up to the real chat-sessions endpoint.")
