import streamlit as st


def check_initialization():
    if "chain" not in st.session_state:
        st.warning("Adicione arquivos .pdf para inicializar o ChatBot")
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
        st.experimental_rerun()


def chat_window():
    st.header(":robot_face: Bem-vindo ao ChatPDF", divider=True)
    check_initialization()

    chain = st.session_state["chain"]
    container = st.container()

    messages = load_chat_history()
    display_chat_history(container, messages)

    new_message = st.chat_input("Converse com seus documentos...")
    process_new_message(container, chain, new_message)