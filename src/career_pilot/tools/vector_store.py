from typing import Optional, List, Tuple
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from career_pilot.core.config import get_embedding_model, get_data_dir


class JDVectorStore:
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
        self.jd_collection: Chroma = Chroma(
            collection_name="job_descriptions",
            embedding_function=embeddings,
            persist_directory=get_data_dir()["chroma"],
        )
        self._initialized = True

    def add_jd(self, jd_text: str, metadata: dict) -> str:
        ids = [str(hash(jd_text))]
        self.jd_collection.add_texts(texts=[jd_text], metadatas=[metadata], ids=ids)
        return ids[0]

    def add_jds(self, jd_list: List[Tuple[str, dict]]) -> List[str]:
        texts, metadatas = zip(*jd_list)
        ids = [str(hash(text)) for text in texts]
        self.jd_collection.add_texts(
            texts=list(texts), metadatas=list(metadatas), ids=ids
        )
        return ids

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        results = self.jd_collection.similarity_search(query, k=top_k)
        return [{"text": doc.page_content, "metadata": doc.metadata} for doc in results]

    def get_by_company(self, company: str) -> List[dict]:
        results = self.jd_collection.get(where={"company": company})
        if not results or not results.get("ids"):
            return []
        return [
            {"text": results["documents"][i], "metadata": results["metadatas"][i]}
            for i in range(len(results["ids"]))
        ]

    def delete_all(self) -> None:
        self.jd_collection.delete(where={})

    def count(self) -> int:
        return self.jd_collection._collection.count()


class CVTemplateStore:
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
        self.template_collection: Chroma = Chroma(
            collection_name="cv_templates",
            embedding_function=embeddings,
            persist_directory=get_data_dir()["chroma"],
        )
        self._initialized = True

    def add_template(self, template_text: str, metadata: dict) -> str:
        ids = [str(hash(template_text))]
        self.template_collection.add_texts(
            texts=[template_text], metadatas=[metadata], ids=ids
        )
        return ids[0]

    def search(self, query: str, top_k: int = 3) -> List[dict]:
        results = self.template_collection.similarity_search(query, k=top_k)
        return [{"text": doc.page_content, "metadata": doc.metadata} for doc in results]

    def delete_all(self) -> None:
        self.template_collection.delete(where={})


def get_jd_store() -> JDVectorStore:
    return JDVectorStore()


def get_template_store() -> CVTemplateStore:
    return CVTemplateStore()
