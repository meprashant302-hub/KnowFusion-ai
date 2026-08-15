"""
views/chat.py
--------------
The main dashboard: greeting, chat thread, quick actions, and the
right-hand "Sources" panel — mirrors the reference product screenshot.

This file is run by app.py's st.navigation(); it should NOT call
st.set_page_config() or render the sidebar itself (both are handled once,
centrally, in app.py / utils/shell.py).
"""

import streamlit as st
from utils import auth, api_client, mock_data
from utils.icons import icon_svg, icon_label

auth.require_auth()
user = auth.current_user()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = list(mock_data.MOCK_CHAT_HISTORY)  # seeded demo thread
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = "chat_001"

main_col, sources_col = st.columns([2.4, 1], gap="large")

# ---------------------------------------------------------------------------
# MAIN COLUMN
# ---------------------------------------------------------------------------
with main_col:
    st.markdown(f"## Hello, {user.get('name', 'there')}!")
    st.markdown("How can I help you today?")
    st.write("")

    chat_container = st.container(height=430, border=False)
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f'<div class="kf-chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(
                        f"<div class='kf-timestamp' style='text-align:right;padding-top:14px;'>{msg['timestamp']}</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f'<div class="kf-chat-assistant">'
                    f'<span style="display:inline-flex;vertical-align:middle;margin-right:6px;">{icon_svg("sparkle", size=15)}</span>'
                    f'{msg["content"].replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True,
                )
                if msg.get("has_web_info"):
                    with st.expander("Additional information from the web", icon=":material/menu_book:"):
                        st.caption("Web-augmented context would appear here once the backend is connected.")

    prompt = st.chat_input("Ask anything about your documents...")
    if prompt:
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt, "timestamp": mock_data.now_display_time()}
        )
        with st.spinner("Thinking..."):
            result = api_client.send_chat_message(
                prompt, st.session_state.active_chat_id, st.session_state.chat_history
            )
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": result["reply"],
                "timestamp": mock_data.now_display_time(),
                "sources_used": result.get("sources_used", []),
                "has_web_info": result.get("has_web_info", False),
            }
        )
        st.session_state.active_chat_id = result.get("chat_id")
        st.rerun()

    st.write("")
    st.markdown("#### Quick Actions")
    qa1, qa2, qa3, qa4 = st.columns(4)
    quick_actions = [
        (qa1, "document", "Summarize", "Get a summary of your documents", "views/summarize.py"),
        (qa2, "compare", "Compare", "Compare multiple documents", "views/compare.py"),
        (qa3, "quiz", "Quiz", "Generate quiz from your content", "views/quiz.py"),
        (qa4, "mindmap", "Mind Map", "Visualize concepts and connections", "views/mindmap.py"),
    ]
    for col, icon_name, title, desc, target in quick_actions:
        with col:
            with st.container(border=True):
                st.markdown(icon_label(icon_name, f"**{title}**", size=18), unsafe_allow_html=True)
                st.caption(desc)
                if st.button("Open", key=f"qa_{icon_name}", use_container_width=True):
                    st.switch_page(target)

# ---------------------------------------------------------------------------
# RIGHT COLUMN — Sources panel
# ---------------------------------------------------------------------------
with sources_col:
    st.markdown(icon_label("stack", "**Sources**", size=18), unsafe_allow_html=True)
    sources = api_client.list_sources()
    for src in sources[:5]:
        badge_class = "kf-badge-pdf" if src["type"].lower() == "pdf" else "kf-badge-docx"
        st.markdown(
            f"""
            <div class="kf-source-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div style="display:flex; gap:8px; align-items:flex-start;">
                        <span class="kf-badge {badge_class}">{src['type'].upper()}</span>
                        <div>
                            <div style="font-weight:600; font-size:0.9rem;">{src['name']}</div>
                            <div class="kf-timestamp">{src['location']}</div>
                        </div>
                    </div>
                    <span class="kf-relevance">{src['relevance']}%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    f'<div class="kf-footer-note">{icon_label("bulb", "Tip: Upload high-quality documents for better results", size=15)}</div>',
    unsafe_allow_html=True,
)
