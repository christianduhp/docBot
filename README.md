# DocBot

DocBot is a chatbot that allows users to interact with documents in various formats, such as PDFs and Excel spreadsheets (.xlsx, .xlsb). It utilizes a Retrieval-Augmented Generation (RAG) architecture to process and respond to questions based on the content of the loaded documents.

![docBOT](https://github.com/user-attachments/assets/76666c7f-57ba-46bc-ade8-9b422846d0e0)
## Project Structure

The project is structured as follows:

```
├── modules
│   ├── rag_pipeline.py
│   ├── chatbot_initialization.py
│   ├── chat_window.py
│   └── sidebar
├── pages
│   └── [Streamlit page files]
├── config
│   └── config.py
├── files
│   └── [Temp files]
├── .env
├── requirements.txt
└── Home.py
```

## Installation

To install the project dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Initialization

To start DocBot:

1. Obtain an API token from Hugginface.
2. Save the token in the .env file as follows:

```bash
HUGGINGFACEHUB_API_TOKEN=your_token_here
```
3. Add PDF, files or CSV and Excel spreadsheets (.xlsx, .xlsb, .csv) to the designated folder.
4. Run the Streamlit application:

```bash
streamlit run Home.py 

# Or

python -m streamlit run Home.py
```

5. In the interface, you can ask questions about the loaded documents.

### `RAGPipeline` Class Structure

The `RAGPipeline` class has the following main methods:

- **`__init__`**: Initializes the pipeline with the directory of files, model name, prompt, retrieval search type, and retrieval parameters.
  
- **`load`**: Loads PDF, CSV, and Excel files from the specified directory. Converts Excel files to CSV when necessary and generates a list of documents for processing.

- **`split`**: Splits documents into smaller chunks to facilitate information retrieval.

- **`embed_and_store`**: Embeds the documents using embedding models and stores the results in a FAISS vector store.

- **`retrieve`**: Creates a retriever to search for relevant documents based on user queries.

- **`generate`**: Generates a conversational chain with a language model and memory.

- **`run`**: Executes the complete pipeline, loading, splitting, embedding, and storing documents.

### Streamlit Functions

- **`initialize_chatbot`**: Initializes the chatbot by checking if there are available files for interaction. Displays error or success messages based on the presence of files.

- **`check_initialization`**: Checks if the chatbot has been initialized correctly.

- **`load_chat_history`**: Loads the chat history of the chatbot.

- **`display_chat_history`**: Displays previous messages in the chatbot interface.

- **`process_new_message`**: Processes new messages sent by the user and generates responses.

- **`chat_window`**: Creates the chatbot interface, allowing user interactions.

## Contributions

Feel free to contribute to the project. To do so, create a new branch, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
