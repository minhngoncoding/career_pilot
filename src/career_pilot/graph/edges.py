from typing import Literal
from career_pilot.graph.state import AppState


def route_by_intent(
    state: AppState,
) -> Literal[
    "cv_analyzer_node",
    "job_matcher_node",
    "skill_gap_node",
    "cv_generator_node",
    "interview_node",
    "greeting_node",
]:
    """Route to appropriate node based on detected intent."""
    intent = state.get("intent", "GREETING")

    intent_to_node = {
        "CV_ANALYSIS": "cv_analyzer_node",
        "JOB_MATCH": "job_matcher_node",
        "SKILL_GAP": "skill_gap_node",
        "CV_GENERATOR": "cv_generator_node",
        "INTERVIEW": "interview_node",
        "GREETING": "greeting_node",
    }
    return intent_to_node.get(intent, "greeting_node")
