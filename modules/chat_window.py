import streamlit as st

from modules.rag_pipeline import RAGPipeline
from config.config import FILES_DIR, get_config

model_name = get_config("model_name")
prompt = get_config("prompt")
retrievel_search_type = get_config("retrievel_search_type")
retrievel_kwargs = get_config("retrievel_kwargs")


def initialize_chatbot(dir):
    if len(list(dir.glob("*"))) == 0:
        st.error("Adicione arquivos para inicializar o DocBot")
    else:
        st.success("Inicializando o DocBot...")
        chat_chain = RAGPipeline(
            FILES_DIR, model_name, prompt, retrievel_search_type, retrievel_kwargs
        ).run()
        st.session_state["chain"] = chat_chain
        st.rerun()


def check_initialization():
    if "chain" not in st.session_state:
        st.warning("Adicione arquivos para inicializar o DocBot")
        st.stop()


def load_chat_history():
    chain = st.session_state["chain"]
    memory = chain.memory
    messages = memory.load_memory_variables({})["chat_history"]
    return messages


def display_chat_history(container, messages):
    for message in messages:
        chat = container.chat_message(message.type)
        chat.markdown(message.content)


def process_new_message(container, chain, new_message):
    if new_message:
        chat = container.chat_message("human")
        chat.markdown(new_message)
        chat = container.chat_message("ai")
        chat.markdown("Gerando nova resposta...")

        response = chain.invoke({"question": new_message})
        st.session_state["last_response"] = response
        st.rerun()


def chat_window():
    st.header(":robot_face: Bem-vindo ao DocBot", divider=True)
    check_initialization()

    chain = st.session_state["chain"]
    container = st.container()

    messages = load_chat_history()
    display_chat_history(container, messages)

    new_message = st.chat_input("Converse com seus documentos...")
    process_new_message(container, chain, new_message)
