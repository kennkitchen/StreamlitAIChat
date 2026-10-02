import sqlite3
import requests
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



class AIEngine:
    def __init__(self):
        self.db = sqlite3.connect("data/app_data.db", check_same_thread=False)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.qdrant = QdrantClient("localhost", port=6333)
        self._init_db()

    def _init_db(self):
        with self.db:
            self.db.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
            self.db.execute("CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, title TEXT, model TEXT)")
            self.db.execute(
                "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, conv_id INTEGER, role TEXT, content TEXT)")

    def get_last_model(self):
        res = self.db.execute("SELECT value FROM settings WHERE key='last_model'").fetchone()
        return res[0] if res else None

    def save_setting(self, key, value):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", (key, value))

    def create_knowledge_base(self, name, files):
        # 1. Load documents (Integrating MinerU/Tesseract would happen here)
        docs = []
        for file in files:
            loader = TextLoader(file)  # Simplified for example
            docs.extend(loader.load())

        # 2. Split text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)

        # 3. Store in Qdrant
        QdrantVectorStore.from_documents(
            splits,
            self.embeddings,
            location="localhost",
            port=6333,
            collection_name=name
        )

    def get_context(self, kb_names, query):
        context = ""
        for name in kb_names:
            vectorstore = QdrantVectorStore(client=self.client, collection_name=name, embeddings=self.embeddings)
            docs = vectorstore.similarity_search(query, k=3)
            context += "\n".join([d.page_content for d in docs])
        return context

    async def stream_response(self, model, query, history, kb_names=None):
        # RAG Logic
        context = ""
        if kb_names:
            for name in kb_names:
                # Use QdrantVectorStore instead of Qdrant
                vs = QdrantVectorStore(
                    client=self.qdrant,
                    collection_name=name,
                    embeddings=self.embeddings
                )
                docs = vs.similarity_search(query, k=2)
                context += "\n".join([d.page_content for d in docs])

        prompt = f"Context: {context}\n\nHistory: {history}\n\nUser: {query}"
        llm = OllamaLLM(model=model)

        for token in llm.stream(prompt):
            yield token
