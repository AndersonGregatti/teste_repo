import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Registro de Frequência — Rede Municipal de Cubatão",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0; padding-left: 1rem; padding-right: 1rem;}
    header[data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

ARQUIVO = Path(__file__).parent / "registro_frequencia_cubatao.html"

if not ARQUIVO.exists():
    st.error(f"Arquivo não encontrado: {ARQUIVO.name}")
    st.stop()

components.html(ARQUIVO.read_text(encoding="utf-8"), height=1200, scrolling=True)