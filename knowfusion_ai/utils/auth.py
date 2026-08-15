"""
auth.py
-------
Session-based auth helper for the Streamlit app.

Streamlit has no built-in concept of "logged in" — it's just a script that
reruns top-to-bottom on every interaction. So "session" here means
`st.session_state`, which persists for the duration of one browser tab.

BACKEND TEAM NOTE:
This currently calls `api_client.login()` / `api_client.signup()`, which are
mocked (see api_client.py). Once the real backend is live and those two
functions return real tokens, you may also want to:
  - Persist the token in `st.session_state["auth_token"]`
  - Send that token as an Authorization header on every subsequent
    `api_client` call that needs auth (most document/chat endpoints will).
No changes should be needed in this file for that — just in api_client.py.
"""

import streamlit as st
from utils import api_client


def init_session_state():
    """Ensure all auth-related keys exist in session_state. Call once per page."""
    defaults = {
        "authenticated": False,
        "user": None,          # dict: {"id", "name", "email"}
        "auth_token": None,
        "auth_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def is_authenticated() -> bool:
    return bool(st.session_state.get("authenticated"))


def current_user() -> dict:
    return st.session_state.get("user") or {"name": "Guest", "email": ""}


def attempt_login(username: str, password: str) -> bool:
    """Try to log in. Returns True on success, sets auth_error on failure."""
    result = api_client.login(username, password)
    if result.get("success"):
        st.session_state.authenticated = True
        st.session_state.user = result.get("user")
        st.session_state.auth_token = result.get("token")
        st.session_state.auth_error = None
        return True
    st.session_state.auth_error = result.get("error", "Login failed. Please try again.")
    return False


def attempt_signup(name: str, email: str, password: str) -> bool:
    """Try to sign up + auto-login. Returns True on success."""
    result = api_client.signup(name, email, password)
    if result.get("success"):
        st.session_state.authenticated = True
        st.session_state.user = result.get("user")
        st.session_state.auth_token = result.get("token")
        st.session_state.auth_error = None
        return True
    st.session_state.auth_error = result.get("error", "Sign up failed. Please try again.")
    return False


def logout():
    """Clear the session and send the user back to the login screen."""
    for key in ("authenticated", "user", "auth_token", "auth_error"):
        st.session_state[key] = None
    st.session_state.authenticated = False


def require_auth():
    """
    Defense-in-depth guard, called at the top of every view.
    Under normal operation views/*.py are only ever reached through
    app.py's st.navigation() (which already gates on auth), so this
    should never actually trigger — it just protects against someone
    running a view file directly.
    """
    init_session_state()
    if not is_authenticated():
        st.warning("Please log in to access KnowFusion AI. Run `streamlit run app.py`.")
        st.stop()
