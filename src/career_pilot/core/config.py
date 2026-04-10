import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def get_ollama_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def get_llm_model() -> str:
    return os.getenv("OLLAMA_MODEL", "llama3.1")


def get_embedding_model() -> str:
    return os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


def get_data_dir() -> dict:
    root = Path(__file__).parent.parent.parent / "data"
    return {
        "chroma": os.getenv("CHROMA_PERSIST_DIR", str(root / "jd_store")),
        "uploads": os.getenv("UPLOAD_DIR", str(root / "uploads")),
    }
