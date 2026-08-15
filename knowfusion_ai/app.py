"""
app.py
------
Single entry point for the KnowFusion AI Streamlit app.

IMPORTANT - why this file looks different from a "normal" multipage app:
Earlier this project used Streamlit's automatic `pages/` folder discovery,
with emoji in the filenames (e.g. "1_Chat.py" with emoji) to control the
icon shown in the nav. That works locally but breaks on some deployment
platforms (including Streamlit Community Cloud) because git checkouts can
normalize emoji/unicode filenames differently (NFC vs NFD), so the filename
`st.switch_page(...)` asks for no longer matches the filename Streamlit
finds on disk -- causing the exact `StreamlitAPIException` you hit.

The fix: don't rely on filenames for navigation at all. This file builds
the navigation *programmatically* with `st.navigation()` + `st.Page()`,
pointing at plain-ASCII files in `views/`. Icons are attached in code, not
encoded into filenames, so this is 100% deploy-safe.

Run with:  streamlit run app.py
"""

import streamlit as st
from utils import auth, ui
from utils.icons import icon_svg

st.set_page_config(
    page_title="KnowFusion AI",
    page_icon="assets/logo.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

auth.init_session_state()
ui.inject_global_css()


# ---------------------------------------------------------------------------
# LOGGED OUT: show the login/signup screen and stop.
# ---------------------------------------------------------------------------
def render_login():
    st.markdown(
        f"""
        <style>
            .kf-login-wrap {{ max-width: 440px; margin: 3rem auto 0 auto; }}
            .kf-login-logo {{ display:flex; justify-content:center; margin-bottom: 0.6rem; }}
            .kf-login-brand {{
                text-align: center; font-size: 1.9rem; font-weight: 800; margin-bottom: 0.2rem;
            }}
            .kf-login-brand span {{ color: {ui.COLORS['accent']}; }}
            .kf-login-sub {{
                text-align: center; color: {ui.COLORS['text_muted']}; margin-bottom: 2rem; font-size: 0.95rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    left, mid, right = st.columns([1, 1.3, 1])
    with mid:
        st.markdown(
            f"""
            <div class="kf-login-logo">{icon_svg('logo', size=44, color=ui.COLORS['accent'], stroke_width=1.5)}</div>
            <div class="kf-login-brand">KnowFusion <span>AI</span></div>
            <div class="kf-login-sub">Your intelligent research assistant, powered by RAG</div>
            """,
            unsafe_allow_html=True,
        )

        tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

        with tab_login:
            with st.form("login_form", border=True):
                username = st.text_input("Email or username", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="********")
                submitted = st.form_submit_button("Log in", use_container_width=True, type="primary")
                if submitted:
                    if auth.attempt_login(username, password):
                        st.rerun()
                    else:
                        st.error(st.session_state.auth_error)
            st.caption("Demo mode: any email + password works (backend not connected yet).")

        with tab_signup:
            with st.form("signup_form", border=True):
                name = st.text_input("Full name", placeholder="Prashant Mishra")
                email = st.text_input("Email", placeholder="you@example.com")
                password_su = st.text_input("Create password", type="password", placeholder="********")
                confirm = st.text_input("Confirm password", type="password", placeholder="********")
                submitted_su = st.form_submit_button("Create account", use_container_width=True, type="primary")
                if submitted_su:
                    if password_su != confirm:
                        st.error("Passwords do not match.")
                    elif auth.attempt_signup(name, email, password_su):
                        st.rerun()
                    else:
                        st.error(st.session_state.auth_error)

        st.markdown(
            '<div class="kf-footer-note">(c) 2026 KnowFusion AI &middot; v1.0.0 &middot; Final Year Project</div>',
            unsafe_allow_html=True,
        )


if not auth.is_authenticated():
    render_login()
    st.stop()


# ---------------------------------------------------------------------------
# LOGGED IN: build the sidebar chrome + navigation, then run the chosen page.
# ---------------------------------------------------------------------------
from utils import shell  # noqa: E402  (imported here so it only loads once authed)

shell.render_top_of_sidebar()  # brand, Upload Document, New Chat

pages = [
    st.Page("views/chat.py", title="Chat", icon=":material/forum:", default=True, url_path="chat"),
    st.Page("views/summarize.py", title="Summarize Document", icon=":material/description:", url_path="summarize"),
    st.Page("views/compare.py", title="Compare Documents", icon=":material/compare_arrows:", url_path="compare"),
    st.Page("views/quiz.py", title="Generate Quiz", icon=":material/quiz:", url_path="quiz"),
    st.Page("views/mindmap.py", title="Mind Map", icon=":material/hub:", url_path="mindmap"),
]
nav = st.navigation(pages, position="sidebar")

shell.render_bottom_of_sidebar()  # help & guides, user info, logout

nav.run()
