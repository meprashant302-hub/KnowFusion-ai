# KnowFusion AI — Frontend (Streamlit)

A RAG-based document assistant. This repo contains the **complete frontend**
only — chat UI, document tools, login/signup, and a documented contract
layer for the backend team to plug into.

## Why the project structure looks like this
This app uses `st.navigation()` + `st.Page()` for multipage routing instead
of Streamlit's automatic `pages/` folder auto-discovery. That's a deliberate
choice: filenames with emoji in a `pages/` folder can get mangled by git's
unicode normalization on deploy (NFC vs NFD), which breaks `st.switch_page`
on platforms like Streamlit Community Cloud. Building navigation
programmatically in `app.py` avoids that class of bug entirely, and lets
icons live in code (`utils/icons.py`) instead of filenames.

## Features implemented (frontend)
- Login / Signup (mock auth, session-based)
- Chat dashboard with source citations panel
- Summarize Document
- Compare Documents
- Generate Quiz (interactive, checkable)
- Mind Map (Graphviz-based concept graph)
- Upload Document (modal, feeds into the Sources list)
- Custom brand logo + a hand-built line-icon set (no emoji, no icon-font
  dependency) for a consistent, original look
- Consistent dark theme matching the product design

## Project structure
```
knowfusion_ai/
├── app.py                  # Single entry point — login screen + st.navigation shell
├── views/                  # Page content only (no page_config/sidebar calls)
│   ├── chat.py              # Main dashboard
│   ├── summarize.py
│   ├── compare.py
│   ├── quiz.py
│   └── mindmap.py
├── utils/
│   ├── auth.py              # Session-state auth helpers
│   ├── api_client.py        # ⭐ BACKEND TEAM: implement real calls here
│   ├── mock_data.py         # Placeholder data (frontend-only)
│   ├── shell.py             # Sidebar chrome (brand, upload, help, logout)
│   ├── icons.py             # Hand-built inline SVG icon set
│   └── ui.py                # Shared CSS/theme + small UI helpers
├── assets/logo.svg          # Standalone brand mark
├── .streamlit/config.toml   # Theme config
└── requirements.txt
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Log in with any non-empty email + password — mock auth accepts anything
while the backend isn't connected yet.

## Backend integration guide
Everything the frontend needs from a backend lives in **`utils/api_client.py`**.
Every function there:
1. Has a docstring documenting the exact expected request/response shape.
2. Currently returns mock data (`USE_MOCK = True`).

To connect a real backend:
1. Build your API (suggested: FastAPI + a vector DB like FAISS/Chroma/Pinecone
   + an LLM provider for generation).
2. Implement each function body in `api_client.py` to call your real
   endpoints via `requests`, keeping the **same return shape**.
3. Set `USE_MOCK = False` (or drive it from an env var).
4. Set `KNOWFUSION_BACKEND_URL` to your API's base URL.

No other file needs to change — `views/*.py` only ever imports from
`api_client.py`, never talks to mock data directly in production paths.

### Suggested endpoints
| Function in api_client.py | Suggested route            |
|---|---|
| `login` | `POST /api/auth/login` |
| `signup` | `POST /api/auth/signup` |
| `upload_document` | `POST /api/documents/upload` |
| `list_sources` | `GET /api/documents` |
| `summarize_document` | `POST /api/documents/summarize` |
| `compare_documents` | `POST /api/documents/compare` |
| `generate_quiz` | `POST /api/documents/quiz` |
| `generate_mind_map` | `POST /api/documents/mindmap` |
| `send_chat_message` | `POST /api/chat` |
| `list_chat_sessions` | `GET /api/chats` |

## Deploying to Streamlit Community Cloud
1. Push this repo to GitHub as-is (no emoji filenames anywhere, so it's safe).
2. On share.streamlit.io, point the app at `app.py` as the main file.
3. That's it — navigation is fully programmatic, so there's nothing else
   to configure.

## Notes for the final report
This frontend was built to be fully demo-able standalone (for
presentations/vivas) using mock data, while keeping a clean seam for
backend integration so both halves of the project can be developed and
graded independently.
