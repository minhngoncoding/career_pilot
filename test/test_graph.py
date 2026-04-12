import pytest
from langchain_core.messages import HumanMessage
from career_pilot.graph.nodes import router_node
from career_pilot.graph.state import AppState


class TestRouterNode:
    @pytest.fixture
    def base_state(self) -> AppState:
        return {"messages": [], "intent": None, "context": {}, "response": None}

    def test_greeting_intent(self, base_state):
        messages = [
            "Hello",
            "Hi there",
            "Can you help me?",
            "What can you do?",
        ]
        for msg in messages:
            state = {**base_state, "messages": [HumanMessage(content=msg)]}
            result = router_node(state)
            assert result["intent"] == "GREETING"

    def test_cv_analysis_intent(self, base_state):
        messages = [
            "Analyze my CV",
            "Check my resume",
            "Score my CV",
            "Review my resume",
        ]
        for msg in messages:
            state = {**base_state, "messages": [HumanMessage(content=msg)]}
            result = router_node(state)
            assert result["intent"] == "CV_ANALYSIS"

    def test_job_match_intent(self, base_state):
        messages = [
            "Find me a job",
            "Search for Python developer positions",
            "Find matching jobs for my profile",
            "What jobs suit me?",
        ]
        for msg in messages:
            state = {**base_state, "messages": [HumanMessage(content=msg)]}
            result = router_node(state)
            assert result["intent"] == "JOB_MATCH"

    def test_skill_gap_intent(self, base_state):
        messages = [
            "What skills do I need?",
            "Analyze skill gaps",
            "What should I learn for data scientist?",
            "Show me my skill gaps",
        ]
        for msg in messages:
            state = {**base_state, "messages": [HumanMessage(content=msg)]}
            result = router_node(state)
            assert result["intent"] == "SKILL_GAP"

    def test_cv_generator_intent(self, base_state):
        messages = [
            "Generate a CV for me",
            "Create a resume",
            "Write my CV",
            "Make a new resume",
        ]
        for msg in messages:
            state = {**base_state, "messages": [HumanMessage(content=msg)]}
            result = router_node(state)
            assert result["intent"] == "CV_GENERATOR"

    def test_interview_intent(self, base_state):
        messages = [
            "Practice interview",
            "Mock interview for frontend",
            "Help me prepare for interview",
            "Interview practice",
        ]
        for msg in messages:
            state = {**base_state, "messages": [HumanMessage(content=msg)]}
            result = router_node(state)
            assert result["intent"] == "INTERVIEW"

    def test_returns_context(self, base_state):
        state = {**base_state, "messages": [HumanMessage(content="test")]}
        result = router_node(state)
        assert "context" in result
        assert isinstance(result["context"], dict)

    def test_complex_prompts_no_keywords(self, base_state):
        """Test LLM-based detection with prompts without obvious keywords."""
        messages = [
            "I want to know if my resume is good enough for applying to senior positions",
            "Looking for opportunities where I can apply my backend skills",
            "What qualifications should I acquire to transition into machine learning?",
            "Create a professional resume tailored for product manager role",
            "I have an interview tomorrow and need to be ready",
        ]
        expected_intents = [
            "CV_ANALYSIS",
            "JOB_MATCH",
            "SKILL_GAP",
            "CV_GENERATOR",
            "INTERVIEW",
        ]
        for msg, expected in zip(messages, expected_intents):
            state = {**base_state, "messages": [HumanMessage(content=msg)]}
            result = router_node(state)
            assert result["intent"] == expected, (
                f"'{msg}' should be {expected}, got {result['intent']}"
            )
