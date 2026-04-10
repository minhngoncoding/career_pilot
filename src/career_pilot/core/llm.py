from langchain_ollama import ChatOllama
from career_pilot.core.config import get_llm_model, get_ollama_url
from typing import Optional

DEFAULT_TEMPERATURE = 0.3


class CareerPilotLLM:
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        base_url: Optional[str] = None,
    ):
        self.model = model or get_llm_model()
        self.temperature = temperature
        self.base_url = base_url or get_ollama_url()
        self._llm = None

    def get_llm(self):
        if self._llm is None:
            self._llm = ChatOllama(
                model=self.model, base_url=self.base_url, temperature=self.temperature
            )
        return self._llm

    def invoke(self, prompt: str, **kwargs):
        return self.get_llm().invoke(prompt, **kwargs)

    def stream(self, prompt: str, **kwargs):
        return self.get_llm().stream(prompt, **kwargs)
