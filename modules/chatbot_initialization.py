import streamlit as st

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from config.config import *


def get_files():
    docs = []
    for file in FILES_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        docs.extend(loader.load())

    return docs


def split_docs(docs):
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500, chunk_overlap=250, separators=["\n\n", "\n", ".", " ", ""]
    )

    docs = recur_splitter.split_documents(docs)

    for i, doc in enumerate(docs):
        doc.metadata["source"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["doc_id"] = i

    return docs


def vector_storize(docs):

    embedding_model = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents=docs, embedding=embedding_model)

    return vector_store


def load_chain(vector_store):
    llm = HuggingFaceEndpoint(repo_id=get_config("model_name"))
    memory = ConversationBufferMemory(
        return_messages=True, memory_key="chat_history", output_key="answer"
    )
    retriever = vector_store.as_retriever(
        search_type=get_config("retrievel_search_type"),
        search_kwargs=get_config("retrievel_kwargs"),
    )
    prompt = PromptTemplate.from_template(get_config("prompt"))

    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        return_source_documents=True,
        verbose=True,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    return chat_chain


def start_chat_chain():

    files = get_files()
    docs = split_docs(files)
    vector_store = vector_storize(docs)
    chat_chain = load_chain(vector_store)

    st.session_state["chain"] = chat_chain

    return chat_chain


def initialize_chatbot(dir):
    if len(list(dir.glob("*.pdf"))) == 0:
        st.error("Adicione arquivos .pdf para inicializar o ChatBot")
    else:
        st.success("Inicializando o ChatBot...")
        start_chat_chain()
        st.rerun()
