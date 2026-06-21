from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from src.config import (
GEMINI_API_KEY,
EMBEDDING_MODEL,
CHROMA_DB_DIR,
COLLECTION_NAME,
CHUNK_SIZE,
CHUNK_OVERLAP,
TOP_K_RESULTS
)

class RAGPipeline:

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GEMINI_API_KEY
        )

        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_DB_DIR,
            embedding_function=self.embeddings
        )

    def load_documents(self):
        documents = []

        data_dir = Path("data")

        for file in data_dir.iterdir():

            try:

                if file.suffix.lower() in [".txt", ".md"]:

                    with open(
                        file,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        text = f.read()

                elif file.suffix.lower() == ".pdf":

                    reader = PdfReader(file)

                    text = ""

                    for page in reader.pages:

                        page_text = page.extract_text()

                        if page_text:
                            text += page_text + "\n"

                else:
                    continue

                documents.append(
                    {
                        "source": file.name,
                        "text": text
                    }
                )

            except Exception as e:

                print(
                    f"Error reading {file.name}: {e}"
                )

        return documents

    def build_index(self):

        docs = self.load_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        texts = []
        metadatas = []

        for doc in docs:

            chunks = splitter.split_text(
                doc["text"]
            )

            for chunk in chunks:

                texts.append(chunk)

                metadatas.append(
                    {
                        "source": doc["source"]
                    }
                )

        if texts:

            self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas
            )

            print(
                f"Indexed {len(texts)} chunks"
            )

    def retrieve_context(
        self,
        query
    ):

        results = self.vector_store.similarity_search_with_score(
            query,
            k=TOP_K_RESULTS
        )

        retrieved = []

        for doc, score in results:

            retrieved.append(
                {
                    "text": doc.page_content,
                    "source": doc.metadata.get(
                        "source",
                        "unknown"
                    ),
                    "score": float(1 - score)
                }
            )

        return retrieved

