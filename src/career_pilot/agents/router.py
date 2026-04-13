import json
from career_pilot.core.llm import CareerPilotLLM
from career_pilot.prompts import ORCHESTRATOR_SYSTEM, ORCHESTRATOR_USER


class Router:
    """Intent detection and routing agent."""

    SUPPORTED_INTENTS = [
        "CV_ANALYSIS",
        "JOB_MATCH",
        "SKILL_GAP",
        "CV_GENERATOR",
        "INTERVIEW",
        "GREETING",
    ]

    def __init__(self):
        self.llm = CareerPilotLLM(temperature=0.1)

    def detect_intent(self, user_message: str) -> dict:
        """Detect user intent from message."""
        prompt = ORCHESTRATOR_USER.format(user_message=user_message)

        response = self.llm.invoke(ORCHESTRATOR_SYSTEM + "\n\n" + prompt)

        try:
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            result = json.loads(content.strip())
            return result
        except (json.JSONDecodeError, AttributeError):
            return self._fallback_detect(user_message)

    def _fallback_detect(self, user_message: str) -> dict:
        """Fallback keyword-based intent detection."""
        msg_lower = user_message.lower()

        if any(kw in msg_lower for kw in ["analyze", "check", "score", "cv", "resume"]):
            return {"intent": "CV_ANALYSIS", "confidence": 0.8, "parameters": {}}
        if any(kw in msg_lower for kw in ["find job", "job", "match"]):
            return {"intent": "JOB_MATCH", "confidence": 0.8, "parameters": {}}
        if any(kw in msg_lower for kw in ["skill", "gap", "learn"]):
            return {"intent": "SKILL_GAP", "confidence": 0.8, "parameters": {}}
        if any(kw in msg_lower for kw in ["generate", "create", "viết", "tạo"]):
            return {"intent": "CV_GENERATOR", "confidence": 0.8, "parameters": {}}
        if any(kw in msg_lower for kw in ["interview", "mock", "practice"]):
            return {"intent": "INTERVIEW", "confidence": 0.8, "parameters": {}}
        if any(kw in msg_lower for kw in ["hello", "hi", "help"]):
            return {"intent": "GREETING", "confidence": 0.9, "parameters": {}}

        return {"intent": "GREETING", "confidence": 0.5, "parameters": {}}

    def route(self, user_message: str) -> str:
        """Route user to appropriate agent."""
        result = self.detect_intent(user_message)
        return result.get("intent", "GREETING")


def get_router() -> Router:
    return Router()
