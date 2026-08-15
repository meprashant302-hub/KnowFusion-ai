"""
shell.py
--------
Sidebar "chrome" — everything around the automatic st.navigation() page
list: the brand header + Upload Document + New Chat at the top, and
Help & Guides + account/logout at the bottom.

Split into render_top_of_sidebar() / render_bottom_of_sidebar() because
app.py inserts st.navigation()'s own page list in between the two calls,
matching the reference layout (brand -> upload -> nav links -> help ->
account).
"""

import streamlit as st
from utils import auth, ui, api_client
from utils.icons import icon_svg, icon_label


@st.dialog("Upload Document")
def _upload_dialog():
    st.caption("PDF or DOCX files only. This goes to the shared knowledge base.")
    file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    if st.button("Upload", type="primary", use_container_width=True, disabled=file is None):
        with st.spinner("Uploading & processing..."):
            result = api_client.upload_document(file.getvalue(), file.name)
        if result.get("success"):
            st.success(f'"{file.name}" uploaded successfully.')
            st.session_state["sources_dirty"] = True
            st.rerun()
        else:
            st.error(result.get("error", "Upload failed."))


def render_top_of_sidebar():
    with st.sidebar:
        ui.brand_header()

        if st.button("Upload Document", use_container_width=True, type="primary", icon=":material/upload:"):
            _upload_dialog()

        if st.button("New Chat", use_container_width=True, icon=":material/add_circle:"):
            st.session_state["chat_history"] = []
            st.session_state["active_chat_id"] = None
            st.rerun()

        ui.section_label("Navigate")


def render_bottom_of_sidebar():
    with st.sidebar:
        ui.section_label("Help & Guides")
        with st.expander("How it works", icon=":material/info:"):
            st.caption(
                "Upload documents, then ask questions in Chat. KnowFusion "
                "retrieves the most relevant passages and generates a "
                "grounded answer, citing its sources."
            )
        with st.expander("Best Practices", icon=":material/description:"):
            st.caption("Upload high-quality, text-based documents for the most accurate answers.")
        with st.expander("Feedback", icon=":material/lightbulb:"):
            st.text_area("Tell us what to improve", label_visibility="collapsed", key="fb_text")
            if st.button("Send feedback", key="fb_send"):
                st.toast("Thanks! (Not yet wired to a backend.)")

        st.divider()
        user = auth.current_user()
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(f"Signed in as **{user.get('name', 'Guest')}**")
        with col2:
            if st.button("", help="Log out", icon=":material/logout:", key="logout_btn"):
                auth.logout()
                st.rerun()

        st.markdown(
            '<div class="kf-footer-note">KnowFusion AI &middot; v1.0.0<br>&copy; 2026</div>',
            unsafe_allow_html=True,
        )
