"""
ui.py
-----
Shared styling + small UI-rendering helpers used across every page, so the
dark theme (colors, cards, chat bubbles, badges) stays consistent app-wide.
Pure presentation — no business logic lives here.
"""

import streamlit as st
from utils.icons import icon_svg

# Central palette (kept in one place so it's easy to re-theme later)
COLORS = {
    "bg": "#0B0F19",
    "surface": "#141A2A",
    "surface_alt": "#1B2338",
    "border": "#232B40",
    "accent": "#3B82F6",
    "accent_soft": "#1E3A8A",
    "text": "#E5E7EB",
    "text_muted": "#94A3B8",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "pdf": "#EF4444",
    "docx": "#3B82F6",
}


def inject_global_css():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {COLORS['bg']};
            }}
            section[data-testid="stSidebar"] {{
                background-color: {COLORS['surface']};
                border-right: 1px solid {COLORS['border']};
            }}
            .kf-brand {{
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 1.35rem;
                font-weight: 800;
                margin-bottom: 1.2rem;
                color: {COLORS['text']};
            }}
            .kf-brand span.accent {{ color: {COLORS['accent']}; }}
            .kf-section-label {{
                text-transform: uppercase;
                font-size: 0.72rem;
                letter-spacing: 0.08em;
                color: {COLORS['text_muted']};
                margin: 1.1rem 0 0.4rem 0;
                font-weight: 700;
            }}
            .kf-card {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 14px;
                padding: 1rem 1.1rem;
                margin-bottom: 0.7rem;
            }}
            .kf-source-card {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 0.7rem 0.8rem;
                margin-bottom: 0.6rem;
            }}
            .kf-badge {{
                display: inline-block;
                font-size: 0.72rem;
                font-weight: 700;
                padding: 0.15rem 0.5rem;
                border-radius: 999px;
                color: white;
            }}
            .kf-badge-pdf {{ background-color: {COLORS['pdf']}; }}
            .kf-badge-docx {{ background-color: {COLORS['docx']}; }}
            .kf-relevance {{
                font-size: 0.72rem;
                font-weight: 700;
                padding: 0.1rem 0.5rem;
                border-radius: 999px;
                background-color: rgba(34,197,94,0.15);
                color: {COLORS['success']};
            }}
            .kf-chat-user {{
                background: linear-gradient(135deg, {COLORS['accent_soft']}, #1D4ED8);
                border-radius: 14px 14px 2px 14px;
                padding: 0.9rem 1.1rem;
                color: white;
                margin: 0.4rem 0;
            }}
            .kf-chat-assistant {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 14px 14px 14px 2px;
                padding: 0.9rem 1.1rem;
                color: {COLORS['text']};
                margin: 0.4rem 0;
            }}
            .kf-timestamp {{
                font-size: 0.7rem;
                color: {COLORS['text_muted']};
            }}
            .kf-quick-action {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 14px;
                padding: 1rem;
                text-align: left;
            }}
            .kf-footer-note {{
                color: {COLORS['text_muted']};
                font-size: 0.8rem;
                text-align: center;
                padding-top: 1rem;
                border-top: 1px solid {COLORS['border']};
                margin-top: 2rem;
            }}
            div[data-testid="stChatInput"] {{
                border-radius: 12px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def brand_header():
    st.markdown(
        f"""
        <div class="kf-brand">
            <span style="color:{COLORS['accent']};display:flex;">{icon_svg('logo', size=26, color=COLORS['accent'])}</span>
            KnowFusion <span class="accent">AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str):
    st.markdown(f'<div class="kf-section-label">{text}</div>', unsafe_allow_html=True)


def relevance_badge(percent: int) -> str:
    return f'<span class="kf-relevance">{percent}%</span>'


def type_badge(doc_type: str) -> str:
    css_class = "kf-badge-pdf" if doc_type.lower() == "pdf" else "kf-badge-docx"
    return f'<span class="kf-badge {css_class}">{doc_type.upper()}</span>'
