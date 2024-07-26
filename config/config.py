import streamlit as st

from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

FILES_DIR = Path(__file__).parent.parent / "files"
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"
RETRIEVEL_SEARCH_TYPE = "mmr"
RETRIEVEL_KWARGS = {"k": 5, "fetch_k": 20}
PROMPT = """Você é um ChatBot amigável que auxilia na interpretação de 
documentos que lhe são fornecidos e SEMPRE responde em português, 
independentemente do idioma da pergunta. 
No contexto fornecido estão as informações dos documentos dos usuários. 
Utilize o contexto para responder as perguntas do usuário. 
Se você não sabe a resposta, apenas diga que não sabe, 
em português e não tente inventar respostas. 
NÃO responda em inglês ou qualquer outro idioma.

Contexto: 
{context}

Conversa Atual: 
{chat_history}

Humano: 
{question}

IA (responda SEMPRE em português): 

        
Contexto: 
{context}

Conversa Atual: 
{chat_history}

Human: 
{question}

AI: 
"""


def get_config(config_name):

    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]

    elif config_name.lower() == "model_name":
        return MODEL_NAME

    elif config_name.lower() == "retrievel_search_type":
        return RETRIEVEL_SEARCH_TYPE

    elif config_name.lower() == "retrievel_kwargs":
        return RETRIEVEL_KWARGS

    elif config_name.lower() == "prompt":
        return PROMPT
