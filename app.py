from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).parent / "files"

st.set_page_config(
    page_title="SmishingGuard - Deteksi SMS Phishing",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hilangkan chrome dan padding bawaan Streamlit agar tampil full-width
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    [data-testid="stVerticalBlock"] {gap: 0;}
    iframe {display: block; border: 0; width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_page() -> str:
    html = (BASE / "index.html").read_text(encoding="utf-8")
    css = (BASE / "style.css").read_text(encoding="utf-8")
    js = (BASE / "script.js").read_text(encoding="utf-8")
    # Inline CSS & JS ke dalam dokumen HTML
    html = html.replace('<link rel="stylesheet" href="style.css">', f"<style>{css}</style>")
    html = html.replace('<script src="script.js"></script>', f"<script>{js}</script>")
    return html


# Render tampilan halaman penuh dengan tinggi dinamis
components.html(load_page(), height=3600, scrolling=False)
