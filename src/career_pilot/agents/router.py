from career_pilot.core.llm import CareerPilotLLM
from career_pilot.prompts import ORCHESTRATOR_SYSTEM, ORCHESTRATOR_USER
from career_pilot.agents.models import (
    IntentDetection,
    IntentParameters,
    SUPPORTED_INTENTS,
)


class Router:
    """Intent detection and routing agent."""

    def __init__(self):
        self._llm = CareerPilotLLM(temperature=0.1)

    @property
    def llm(self):
        return self._llm.with_structured_output(IntentDetection)

    def detect_intent(self, user_message: str) -> IntentDetection:
        prompt = ORCHESTRATOR_USER.format(user_message=user_message)
        try:
            return self.llm.invoke(ORCHESTRATOR_SYSTEM + "\n\n" + prompt)
        except Exception:
            return self._fallback_detect(user_message)

    def _fallback_detect(self, user_message: str) -> IntentDetection:
        """Fallback keyword-based intent detection."""
        msg_lower = user_message.lower()
        params = IntentParameters()

        if any(kw in msg_lower for kw in ["analyze", "check", "score", "cv", "resume"]):
            return IntentDetection(
                intent="CV_ANALYSIS", confidence=0.8, parameters=params
            )
        if any(kw in msg_lower for kw in ["find job", "job", "match"]):
            return IntentDetection(
                intent="JOB_MATCH", confidence=0.8, parameters=params
            )
        if any(kw in msg_lower for kw in ["skill", "gap", "learn"]):
            return IntentDetection(
                intent="SKILL_GAP", confidence=0.8, parameters=params
            )
        if any(kw in msg_lower for kw in ["generate", "create", "viết", "tạo"]):
            return IntentDetection(
                intent="CV_GENERATOR", confidence=0.8, parameters=params
            )
        if any(kw in msg_lower for kw in ["interview", "mock", "practice"]):
            return IntentDetection(
                intent="INTERVIEW", confidence=0.8, parameters=params
            )
        if any(kw in msg_lower for kw in ["hello", "hi", "help"]):
            return IntentDetection(intent="GREETING", confidence=0.9, parameters=params)

        return IntentDetection(intent="GREETING", confidence=0.5, parameters=params)

    def route(self, user_message: str) -> IntentDetection:
        """Route user to appropriate agent."""
        return self.detect_intent(user_message)


def get_router() -> Router:
    return Router()
