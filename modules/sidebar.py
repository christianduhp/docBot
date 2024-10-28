import streamlit as st
from modules.chat_window import initialize_chatbot


def sidebar(dir):
    uploaded_files = st.file_uploader(
        ":heavy_plus_sign: Adicione um ou mais arquivos",
        type=[".pdf", ".xlsx", ".csv", ".xlsb"],
        accept_multiple_files=True,
    )

    if not uploaded_files is None:
        delete_all_files(dir)
        save_uploaded_files(uploaded_files, dir)

    initialize_or_update_chatbot(dir)


def save_uploaded_files(uploaded_files, dir):
    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)

    for pdf in uploaded_files:
        with open(dir / pdf.name, "wb") as f:
            f.write(pdf.read())


def delete_all_files(dir):
    for file in dir.glob("*"):
        file.unlink()


def initialize_or_update_chatbot(dir):
    label_btn = ":arrow_forward: Inicializar DocBot"
    if "chain" in st.session_state:
        label_btn = ":arrows_counterclockwise: Atualizar DocBot"

    if st.button(label_btn, use_container_width=True):
        initialize_chatbot(dir)
