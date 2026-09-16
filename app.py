import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Registro de Frequência — Rede Municipal de Cubatão",
    page_icon="📋",
    layout="wide",
)

ARQUIVO = Path(__file__).parent / "registro_frequencia_cubatao.html"

if not ARQUIVO.exists():
    st.error(f"Arquivo não encontrado: {ARQUIVO.name}")
    st.stop()

html = ARQUIVO.read_text(encoding="utf-8")

components.html(html, height=1400, scrolling=True)