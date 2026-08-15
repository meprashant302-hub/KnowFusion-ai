"""
icons.py
--------
Small, hand-authored line-icon set used across the whole app instead of
emoji. Every icon is a plain inline SVG (24x24 viewbox, currentColor
stroke) so it always inherits the surrounding text color and scales
cleanly at any size — no external icon font, no emoji-rendering
inconsistencies across OS/browser, and no filename issues on deploy.
"""

_ICON_PATHS = {
    # Brand mark: a small "knowledge graph" — a fused center node wired to
    # three outer nodes. Used everywhere the emoji "🔷" used to be.
    "logo": """
        <line x1="12" y1="13" x2="6" y2="17" stroke-width="1.6"/>
        <line x1="12" y1="13" x2="18" y2="17" stroke-width="1.6"/>
        <line x1="12" y1="13" x2="12" y2="8.4" stroke-width="1.6"/>
        <circle cx="6" cy="17" r="2.3"/>
        <circle cx="18" cy="17" r="2.3"/>
        <circle cx="12" cy="6" r="2.3"/>
        <circle cx="12" cy="13" r="1.7" fill="currentColor" stroke="none"/>
    """,
    "chat": """
        <path d="M4.5 5.5c0-.83.67-1.5 1.5-1.5h12c.83 0 1.5.67 1.5 1.5v9
                 c0 .83-.67 1.5-1.5 1.5H9l-4 3.4V16h-.5c-.83 0-1.5-.67-1.5-1.5v-9Z"/>
        <line x1="7.3" y1="8.6" x2="16.7" y2="8.6"/>
        <line x1="7.3" y1="11.6" x2="13" y2="11.6"/>
    """,
    "document": """
        <path d="M7 3h6.5L18 7.5V20a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/>
        <path d="M13.5 3v4.5H18"/>
        <line x1="9" y1="12.2" x2="15" y2="12.2"/>
        <line x1="9" y1="15.4" x2="15" y2="15.4"/>
        <line x1="9" y1="18.6" x2="12.5" y2="18.6"/>
    """,
    "compare": """
        <path d="M4 8h9.5"/>
        <path d="M11 5l2.5 3-2.5 3"/>
        <path d="M20 16h-9.5"/>
        <path d="M13 19l-2.5-3 2.5-3"/>
    """,
    "quiz": """
        <circle cx="12" cy="12" r="9"/>
        <path d="M9.6 9.2a2.4 2.4 0 1 1 3.3 2.2c-.7.3-1.1.9-1.1 1.7v.4"/>
        <circle cx="11.85" cy="16.3" r="0.95" fill="currentColor" stroke="none"/>
    """,
    "mindmap": """
        <circle cx="12" cy="12" r="2.3"/>
        <circle cx="4.2" cy="5.5" r="1.9"/>
        <circle cx="19.8" cy="5.5" r="1.9"/>
        <circle cx="4.2" cy="18.5" r="1.9"/>
        <circle cx="19.8" cy="18.5" r="1.9"/>
        <line x1="5.7" y1="6.8" x2="10.3" y2="10.5"/>
        <line x1="18.3" y1="6.8" x2="13.7" y2="10.5"/>
        <line x1="5.7" y1="17.2" x2="10.3" y2="13.5"/>
        <line x1="18.3" y1="17.2" x2="13.7" y2="13.5"/>
    """,
    "upload": """
        <path d="M12 15.5V4.2"/>
        <path d="M7.8 8.4 12 4.2l4.2 4.2"/>
        <path d="M4.5 15.5v3a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-3"/>
    """,
    "new": """
        <circle cx="12" cy="12" r="9"/>
        <line x1="12" y1="7.8" x2="12" y2="16.2"/>
        <line x1="7.8" y1="12" x2="16.2" y2="12"/>
    """,
    "info": """
        <circle cx="12" cy="12" r="9"/>
        <line x1="12" y1="11" x2="12" y2="16.3"/>
        <circle cx="12" cy="7.6" r="0.95" fill="currentColor" stroke="none"/>
    """,
    "bulb": """
        <path d="M9.2 18.2h5.6"/>
        <path d="M10.1 21h3.8"/>
        <path d="M12 3.2a5.8 5.8 0 0 0-3.4 10.5c.5.4.8 1 .8 1.6v.4h5.2v-.4c0-.6.3-1.2.8-1.6A5.8 5.8 0 0 0 12 3.2Z"/>
    """,
    "logout": """
        <path d="M9.5 4.3H6.3a2 2 0 0 0-2 2v11.4a2 2 0 0 0 2 2h3.2"/>
        <path d="M15.8 16.5 20 12.3l-4.2-4.2"/>
        <line x1="20" y1="12.3" x2="9" y2="12.3"/>
    """,
    "lock": """
        <rect x="5" y="10.8" width="14" height="9.2" rx="1.6"/>
        <path d="M8 10.8V7.4a4 4 0 0 1 8 0v3.4"/>
    """,
    "key": """
        <circle cx="7.2" cy="15.3" r="3.4"/>
        <path d="M9.7 12.7 18.6 3.8"/>
        <path d="M15 7.4l2.4 2.4"/>
        <path d="M17.6 4.8l1.9 1.9"/>
    """,
    "sparkle": """
        <path d="M12 3.4 13.3 8 18 9.3l-4.7 1.3L12 15.2l-1.3-4.6L6 9.3l4.7-1.3L12 3.4Z"/>
        <path d="M18.7 14.6l.55 1.85 1.85.55-1.85.55-.55 1.85-.55-1.85-1.85-.55 1.85-.55Z"/>
    """,
    "book": """
        <path d="M12 6.5c-1.8-1.4-4.4-2.1-7.3-2.1v13.4c2.9 0 5.5.7 7.3 2.1
                 1.8-1.4 4.4-2.1 7.3-2.1V4.4c-2.9 0-5.5.7-7.3 2.1Z"/>
        <line x1="12" y1="6.5" x2="12" y2="19.9"/>
    """,
    "stack": """
        <rect x="4.5" y="4" width="15" height="4.2" rx="1"/>
        <rect x="4.5" y="10" width="15" height="4.2" rx="1"/>
        <rect x="4.5" y="16" width="9" height="4.2" rx="1"/>
    """,
    "arrow-right": """
        <line x1="4.5" y1="12" x2="18" y2="12"/>
        <path d="M13.5 6.5 19 12l-5.5 5.5"/>
    """,
}


def icon_svg(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 1.7) -> str:
    """Return a standalone inline <svg> string for the named icon."""
    inner = _ICON_PATHS.get(name, "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'width="{size}" height="{size}" fill="none" stroke="{color}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
        f"{inner}</svg>"
    )


def icon_label(name: str, label: str, size: int = 17, gap: str = "0.55rem") -> str:
    """Icon + text inline, for use inside st.markdown(..., unsafe_allow_html=True)."""
    return (
        f'<span style="display:inline-flex;align-items:center;gap:{gap};">'
        f"{icon_svg(name, size=size)}<span>{label}</span></span>"
    )
