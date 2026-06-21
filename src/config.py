import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHAT_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/gemini-embedding-001"

CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "support_kb"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

TOP_K_RESULTS = 3

CONFIDENCE_THRESHOLD = 0.30

SENSITIVE_TOPICS = [
    "refund",
    "billing",
    "duplicate charge",
    "payment dispute",
    "legal",
    "lawsuit",
    "account deletion"
]