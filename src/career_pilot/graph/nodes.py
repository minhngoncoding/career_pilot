from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage
from career_pilot.graph.state import AppState
from career_pilot.agents.router import get_router
from career_pilot.prompts.prompt_templates import (
    CV_ANALYZER_SYSTEM,
    CV_ANALYZER_USER,
    JOB_MATCHER_SYSTEM,
    JOB_MATCHER_USER,
    SKILL_GAP_SYSTEM,
    SKILL_GAP_USER,
    CV_GENERATOR_SYSTEM,
    CV_GENERATOR_USER,
    INTERVIEW_SYSTEM,
    INTERVIEW_USER,
)
from career_pilot.core.llm import CareerPilotLLM

router = get_router()
llm = CareerPilotLLM(temperature=0.3)


def router_node(state: AppState) -> dict:
    last_msg = state["messages"][-1].content
    intent = router.route(last_msg)
    return {"intent": intent, "context": {}}


def cv_analyzer_node(state: AppState) -> dict:
    """Placeholder for CV analyzer node."""
    last_msg = state["messages"][-1].content
    prompt = CV_ANALYZER_USER.format(cv_text=last_msg, target_jd_section="")
    response = llm.invoke(CV_ANALYZER_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def job_matcher_node(state: AppState) -> dict:
    """Placeholder for job matcher node."""
    last_msg = state["messages"][-1].content
    prompt = JOB_MATCHER_USER.format(cv_text=last_msg, target_role="", location="")
    response = llm.invoke(JOB_MATCHER_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def skill_gap_node(state: AppState) -> dict:
    """Placeholder for skill gap node."""
    last_msg = state["messages"][-1].content
    prompt = SKILL_GAP_USER.format(cv_text=last_msg, target_role="")
    response = llm.invoke(SKILL_GAP_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def cv_generator_node(state: AppState) -> dict:
    """Placeholder for CV generator node."""
    last_msg = state["messages"][-1].content
    prompt = CV_GENERATOR_USER.format(jd_text=last_msg, cv_text="", additional_info="")
    response = llm.invoke(CV_GENERATOR_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def interview_node(state: AppState) -> dict:
    """Placeholder for interview node."""
    last_msg = state["messages"][-1].content
    prompt = INTERVIEW_USER.format(position=last_msg, company="", cv_text="")
    response = llm.invoke(INTERVIEW_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def greeting_node(state: AppState) -> dict:
    """Greeting node - responds to general queries."""
    greeting = (
        "👋 Hello! I'm Career Pilot, your AI career assistant. I can help you with:\n\n"
    )
    greeting += "• CV Analysis - Analyze and improve your resume\n"
    greeting += "• Job Matching - Find suitable jobs based on your profile\n"
    greeting += "• Skill Gap - Identify skills you need to develop\n"
    greeting += "• CV Generation - Create a professional CV\n"
    greeting += "• Interview Prep - Practice for job interviews\n\n"
    greeting += "How can I help you today?"
    return {"response": greeting}


def end_node(state: AppState) -> dict:
    """End node - returns final response."""
    return {"response": state.get("response", "Done")}
