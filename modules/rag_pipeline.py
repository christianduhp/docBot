import pandas as pd

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate


class RAGPipeline:
    def __init__(
        self, files_dir, model_name, prompt, retrievel_search_type, retrievel_kwargs
    ):

        self.files_dir = files_dir
        self.model_name = model_name
        self.prompt = prompt
        self.retrievel_search_type = retrievel_search_type
        self.retrievel_kwargs = retrievel_kwargs
        self.embed_model_name = "all-MiniLM-L6-v2"

    def load(self):
        files = []

        try:
            # Process PDF files
            for file in self.files_dir.glob("*.pdf"):
                loader = PyPDFLoader(str(file))
                files.extend(loader.load())
                print(f"Loaded PDF: {file}")

            # Process Excel files
            for file in self.files_dir.glob("*.xlsx"):
                df = pd.read_excel(file)
                csv_path = file.with_suffix(".csv")
                df.to_csv(csv_path, index=False)
                print(f"Converted and loaded Excel: {file}")

            # Process .xlsb files
            for file in self.files_dir.glob("*.xlsb"):
                df = pd.read_excel(file, engine="pyxlsb")
                csv_path = file.with_suffix(".csv")
                df.to_csv(csv_path, index=False)
                print(f"Converted and loaded XLSB: {file}")

            # Process CSV files
            for file in self.files_dir.glob("*.csv"):
                loader = CSVLoader(str(file), encoding="utf-8")
                files.extend(loader.load())
                print(f"Loaded CSV: {file}")

        except Exception as e:
            print(f"Error loading files: {e}")

        if not files:
            raise ValueError(
                "No files were loaded. Please ensure there are supported file types in the directory."
            )

        return files

    def split(self, files):
        recur_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500, chunk_overlap=250, separators=["\n\n", "\n", ".", " ", ""]
        )

        docs = recur_splitter.split_documents(files)

        for i, doc in enumerate(docs):
            doc.metadata["source"] = doc.metadata["source"].split("/")[-1]
            doc.metadata["doc_id"] = i

        return docs

    def embed_and_store(self, docs):
        embedding_model = HuggingFaceBgeEmbeddings(model_name=self.embed_model_name)
        vectorstore = FAISS.from_documents(documents=docs, embedding=embedding_model)
        return vectorstore

    def retrieve(self, vectorstore):
        retriever = vectorstore.as_retriever(
            search_type=self.retrievel_search_type, search_kwargs=self.retrievel_kwargs
        )
        return retriever

    def generate(self, retriver):
        llm = HuggingFaceEndpoint(repo_id=self.model_name)
        memory = ConversationBufferMemory(
            return_messages=True, memory_key="chat_history", output_key="answer"
        )

        prompt = PromptTemplate.from_template(self.prompt)

        chat_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            memory=memory,
            return_source_documents=True,
            verbose=True,
            retriever=retriver,
            combine_docs_chain_kwargs={"prompt": prompt},
        )

        return chat_chain

    def run(self):
        files = self.load()
        docs = self.split(files)
        vectorstore = self.embed_and_store(docs)
        retriver = self.retrieve(vectorstore)
        chat_chain = self.generate(retriver)
        return chat_chain
