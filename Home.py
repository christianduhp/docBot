import streamlit as st

from modules.sidebar import sidebar
from modules.chat_window import chat_window

from config.config import FILES_DIR


def main():
    with st.sidebar:
        sidebar(FILES_DIR)
    chat_window()


if __name__ == "__main__":
    main()
