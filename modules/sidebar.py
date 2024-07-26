import streamlit as st
from modules.chatbot_initialization import initialize_chatbot


def sidebar(dir):
    uploaded_pdfs = st.file_uploader(
        "Adicione arquivos pdf", type=[".pdf"], accept_multiple_files=True
    )
    
    if not uploaded_pdfs is None:
        delete_all_pdf_files(dir)
        save_uploaded_pdfs(uploaded_pdfs, dir)

    initialize_or_update_chatbot(dir)


def save_uploaded_pdfs(uploaded_pdfs, dir):
    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)

    for pdf in uploaded_pdfs:
        with open(dir / pdf.name, "wb") as f:
            f.write(pdf.read())


def delete_all_pdf_files(dir):
    for file in dir.glob("*.pdf"):
        file.unlink()


def initialize_or_update_chatbot(dir):
    label_btn = "Inicializar ChatBot"
    if "chain" in st.session_state:
        label_btn = "Atualizar ChatBot"

    if st.button(label_btn, use_container_width=True):
        initialize_chatbot(dir)
