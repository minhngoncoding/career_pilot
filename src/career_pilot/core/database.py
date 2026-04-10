from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from career_pilot.core.config import get_embedding_model, get_data_dir


class VectorDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        embeddings = HuggingFaceEmbeddings(model_name=get_embedding_model())
        self.client: Chroma = Chroma(
            client_type="persistent",
            embedding_function=embeddings,
            persist_directory=get_data_dir()["chroma"],
        )
        self._initialized = True

    def get_client(self) -> Chroma:
        return self.client

    def get_collection(self, name: str) -> Chroma:
        return Chroma(
            client_type="persistent",
            collection_name=name,
            embedding_function=HuggingFaceEmbeddings(model_name=get_embedding_model()),
            persist_directory=get_data_dir()["chroma"],
        )

    def reset(self) -> None:
        self.client.delete_collection()
        self._initialized = False


def get_database() -> VectorDatabase:
    return VectorDatabase()
