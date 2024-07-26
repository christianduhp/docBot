
# ChatPDF - Conversational AI with PDF Documents

This project uses Streamlit to create a conversational AI application that can interpret and respond to queries based on PDF documents uploaded by the user. The app is designed to allow users to change the prompt and parameters in the "Configurações" (Settings).

## Features

- Upload multiple PDF files to initialize or update the chatbot
- Conversational AI that interprets and responds to questions based on the content of the uploaded PDFs
- Uses `langchain` and `huggingface` for embedding and retrieval
- Maintains a conversation history

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/christianduhp/ChatPDF.git
    cd ChatPDF
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add the necessary environment variables:
    ```env
    HUGGINGFACEHUB_API_TOKEN=YOUR_TOKEN
    ```

## Usage

1. Start the Streamlit application:
    ```bash
    streamlit run Home.py
    ```

2. In the Streamlit web interface:
    - Upload one or more PDF files using the file uploader in the sidebar.
    - Click the "Inicializar ChatBot" button to initialize the chatbot.
    - Interact with the chatbot by typing questions in the input field. The chatbot will respond based on the content of the uploaded PDFs.


## Contributing

Feel free to submit issues, fork the repository, and make pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
