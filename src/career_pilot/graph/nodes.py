from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage
from career_pilot.graph.state import AppState
from career_pilot.agents.router import Router
from career_pilot.agents.cv_analyzer import CVAnalyzer
from career_pilot.agents.job_matcher import JobMatcher
from career_pilot.prompts.prompt_templates import (
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
from career_pilot.tools.cv_parser import parse_resume

router = Router()
cv_analyzer = CVAnalyzer()
job_matcher = JobMatcher()
llm = CareerPilotLLM(temperature=0.3)


def router_node(state: AppState) -> dict:
    """Router node - only detects intent, no extraction."""
    last_msg = state["messages"][-1].content
    result = router.route(last_msg)
    return {"intent": result.intent}


def cv_analyzer_node(state: AppState) -> dict:
    """Analyze CV with user request consideration."""
    last_msg = state["messages"][-1].content  # User message
    files = state.get("files", [])
    user_request = last_msg  # Full user message as request

    # Get CV content from files
    cv_text = ""
    for file in files:
        cv_text += parse_resume(file) + "\n\n"

    # If no files, check if user pasted CV in message (simple detection)
    if not cv_text and len(last_msg) > 200:
        # Assume user pasted their CV in the message
        cv_text = last_msg
        user_request = "Analyze my CV"

    result = cv_analyzer.analyze_cv(cv_text=cv_text, user_request=user_request)

    # Store CV context for memory
    cv_context = {
        "cv_text": cv_text,
        "user_request": user_request,
        "analysis": result,
    }

    return {"response": result, "cv_context": cv_context}


def job_matcher_node(state: AppState) -> dict:
    """Match user CV to available job descriptions."""
    last_msg = state["messages"][-1].content
    files = state.get("files", [])
    cv_context = state.get("cv_context", {})

    # Get CV text from files or context
    cv_text = ""

    # 1. Try to get from files
    for file in files:
        cv_text += parse_resume(file) + "\n\n"

    # 2. Try to get from CV context (from previous CV analysis)
    if not cv_text and cv_context.get("cv_text"):
        cv_text = cv_context["cv_text"]

    # 3. If still no CV, check if user pasted in message
    if not cv_text and len(last_msg) > 200:
        cv_text = last_msg

    # Extract target role and location from message if present
    target_role = None
    location = None

    # Simple extraction (could be improved with NLP)
    msg_lower = last_msg.lower()
    if " in " in last_msg:
        parts = last_msg.split(" in ")
        if len(parts) > 1:
            location = parts[-1].strip()
            last_msg = parts[0].strip()

    # Match jobs
    result = job_matcher.match(
        cv_text=cv_text,
        target_role=target_role,
        location=location,
        top_k=5,
    )

    # Format response
    response = _format_job_matches(result)
    return {"response": response}


def skill_gap_node(state: AppState) -> dict:
    """TODO: Parse files from state when needed"""
    last_msg = state["messages"][-1].content
    files = state.get("files", [])
    # TODO: Parse files when available
    prompt = SKILL_GAP_USER.format(cv_text=last_msg, jd_text="")
    response = llm.invoke(SKILL_GAP_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def cv_generator_node(state: AppState) -> dict:
    """TODO: Parse files from state when needed"""
    last_msg = state["messages"][-1].content
    files = state.get("files", [])
    # TODO: Parse files when available
    prompt = CV_GENERATOR_USER.format(jd_text=last_msg, cv_text="", additional_info="")
    response = llm.invoke(CV_GENERATOR_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def interview_node(state: AppState) -> dict:
    """TODO: Parse files from state when needed"""
    last_msg = state["messages"][-1].content
    files = state.get("files", [])
    # TODO: Parse files when available
    prompt = INTERVIEW_USER.format(position=last_msg, company="", cv_text="")
    response = llm.invoke(INTERVIEW_SYSTEM + "\n\n" + prompt)
    return {"response": response.content}


def greeting_node(state: AppState) -> dict:
    """TODO: Check if files exist in state and ask for clarification

    Example:
        files = state.get("files", [])
        if files:
            return "👋 Hello! I see you uploaded a file. What would you like me to do with it?"
    """
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


def _format_job_matches(result) -> str:
    """Format job match results for display."""
    if not result.matches:
        return f"🔍 No matching jobs found.\n\n{result.recommendations}"

    output = "🎯 **Job Matches Found**\n\n"

    for job in result.matches:
        output += f"**{job.rank}. {job.job_title}** @ {job.company}\n"
        output += f"📍 {job.location} | 📊 Match Score: {job.match_score}%\n\n"

        if job.matched_skills:
            output += f"✅ Matched Skills: {', '.join(job.matched_skills[:5])}\n"
        if job.missing_skills:
            output += f"❌ Missing Skills: {', '.join(job.missing_skills[:5])}\n"

        output += "\n---\n\n"

    output += f"💡 **Recommendations:**\n{result.recommendations}"
    return output
