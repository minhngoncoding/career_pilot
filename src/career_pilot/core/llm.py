from langchain_ollama import ChatOllama
from langchain_core.language_models import BaseChatModel
from career_pilot.core.config import get_llm_model, get_ollama_url
from typing import Optional, Type, TypeVar, Any
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

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

    def get_llm(self) -> ChatOllama:
        if self._llm is None:
            self._llm = ChatOllama(
                model=self.model, base_url=self.base_url, temperature=self.temperature
            )
        return self._llm

    def invoke(self, prompt: str, **kwargs) -> Any:
        return self.get_llm().invoke(prompt, **kwargs)

    def stream(self, prompt: str, **kwargs):
        return self.get_llm().stream(prompt, **kwargs)

    def with_structured_output(self, model: Type[T], **kwargs) -> Any:
        """Return a chain that outputs the given Pydantic model."""
        return self.get_llm().with_structured_output(model, **kwargs)
