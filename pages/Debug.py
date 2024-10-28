import streamlit as st
from config.config import get_config
from langchain.prompts import PromptTemplate

def debug_page():
    st.header("Página de debug", divider=True)
    prompt_template = get_config('prompt')
    prompt_template = PromptTemplate.from_template(prompt_template)
    
    if not 'last_response' in st.session_state:
        st.warning('Realize uma pergunta para o modelo para visualizar o debug')
        st.stop()

    last_response = st.session_state["last_response"]

    context_docs = last_response['source_documents']
    context_list = [doc.page_content for doc in context_docs]
    context_str = '\n\n'.join(context_list)

    chain = st.session_state['chain']
    memory = chain.memory
    chat_history = memory.buffer_as_str

    with st.container(border=True):

        prompt = prompt_template.format(
            chat_history=chat_history,
            context=context_str,
            question=''
        )

        st.code(prompt)

    st.write(prompt_template)
    st.write(last_response)   

    

debug_page()
