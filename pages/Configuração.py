import json
import streamlit as st
from config.config import get_config, FILES_DIR
from modules.sidebar import initialize_chatbot


def config_page():
    st.header("Página de configuração", divider=True)

    model_name = st.text_input("Modifique o modelo", value=get_config("model_name"))
    retrievel_search_type = st.text_input(
        "Modifique o tipo de retrievel", value=get_config("retrievel_search_type")
    )
    retrievel_kwargs = st.text_input(
        "Modifique os parâmetros de retrievel", value=get_config("retrievel_kwargs")
    )
    prompt = st.text_area(
        "Modifique o prompt padrão", height=350, value=get_config("prompt")
    )

    if st.button("Atualizar parâmetros e rodar Chat", use_container_width=True):
        retrievel_kwargs = json.loads(retrievel_kwargs.replace("'", '"'))
        st.session_state["model_name"] = model_name
        st.session_state["retrievel_search_type"] = retrievel_search_type
        st.session_state["retrievel_kwargs"] = retrievel_kwargs
        st.session_state["prompt"] = prompt
        st.rerun()
        initialize_chatbot(FILES_DIR)


config_page()
