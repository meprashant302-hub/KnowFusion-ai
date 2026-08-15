"""
mock_data.py
------------
FRONTEND-ONLY placeholder data.

Everything in this file exists so the UI has something to render before the
real backend/RAG pipeline is wired up. The shape of each mock object is
intentionally designed to match the response shape documented in
`utils/api_client.py`.

BACKEND TEAM: once your endpoints are live, you don't need to touch this
file at all — just implement the functions in `api_client.py` to call your
real API instead of returning these mocks. The rest of the app (pages/*)
only ever talks to `api_client.py`, never to this file directly, except
during local frontend-only development/demo mode.
"""

from datetime import datetime

# ---------------------------------------------------------------------------
# Sample uploaded documents (right-hand "Sources" panel + Upload Document list)
# ---------------------------------------------------------------------------
MOCK_SOURCES = [
    {
        "id": "src_001",
        "name": "AI_Notes.pdf",
        "type": "pdf",
        "location": "Page 12",
        "relevance": 92,
        "uploaded_at": "2026-08-01T10:00:00",
    },
    {
        "id": "src_002",
        "name": "DBMS_Handbook.pdf",
        "type": "pdf",
        "location": "Page 33",
        "relevance": 87,
        "uploaded_at": "2026-08-02T10:00:00",
    },
    {
        "id": "src_003",
        "name": "Research_Paper.pdf",
        "type": "pdf",
        "location": "Page 5",
        "relevance": 82,
        "uploaded_at": "2026-08-03T10:00:00",
    },
    {
        "id": "src_004",
        "name": "LangChain Documentation.docx",
        "type": "docx",
        "location": "docs.langchain.com",
        "relevance": 76,
        "uploaded_at": "2026-08-04T10:00:00",
    },
    {
        "id": "src_005",
        "name": "Python_Notes.docx",
        "type": "docx",
        "location": "Page 8",
        "relevance": 71,
        "uploaded_at": "2026-08-05T10:00:00",
    },
]

# ---------------------------------------------------------------------------
# Sample chat history for the default/demo conversation
# ---------------------------------------------------------------------------
MOCK_CHAT_HISTORY = [
    {
        "role": "user",
        "content": "Explain what Retrieval-Augmented Generation (RAG) is.",
        "timestamp": "10:32 AM",
    },
    {
        "role": "assistant",
        "content": (
            "Retrieval-Augmented Generation (RAG) is an AI framework that "
            "combines information retrieved from external knowledge sources "
            "with the text generation capabilities of large language models "
            "(LLMs) to produce more accurate, relevant, and contextually "
            "aware responses.\n\n"
            "It works by first retrieving relevant documents or passages "
            "from a knowledge base (your uploaded files in this case) and "
            "then using that retrieved information to generate a "
            "well-informed answer."
        ),
        "timestamp": "10:32 AM",
        "sources_used": ["src_001", "src_004"],
        "has_web_info": True,
    },
]

MOCK_CHAT_SESSIONS = [
    {"id": "chat_001", "title": "RAG Fundamentals", "updated_at": "2026-08-11T10:32:00"},
    {"id": "chat_002", "title": "DBMS Normalization Q&A", "updated_at": "2026-08-10T16:12:00"},
    {"id": "chat_003", "title": "LangChain vs LlamaIndex", "updated_at": "2026-08-09T09:05:00"},
]


def now_display_time() -> str:
    """Return current time formatted like '10:32 AM' for demo chat bubbles."""
    return datetime.now().strftime("%I:%M %p").lstrip("0")
