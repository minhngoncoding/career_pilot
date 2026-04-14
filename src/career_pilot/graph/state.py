from typing import TypedDict, List, Optional, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


class AppState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    intent: Optional[str]
    files: Optional[list]
    cv_context: Optional[dict]  # Store parsed CV info for memory
    response: Optional[str]
