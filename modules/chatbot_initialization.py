import streamlit as st

from modules.rag_pipeline import RAGPipeline


def initialize_chatbot(dir):
    if len(list(dir.glob("*.pdf"))) == 0:
        st.error("Adicione arquivos .pdf para inicializar o DocBot")
    else:
        st.success("Inicializando o DocBot...")
        chat_chain = RAGPipeline().run()
        st.session_state["chain"] = chat_chain
        st.rerun()
