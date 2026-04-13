from langgraph.graph import StateGraph, START, END
from career_pilot.graph.state import AppState
from career_pilot.graph.nodes import (
    router_node,
    cv_analyzer_node,
    job_matcher_node,
    skill_gap_node,
    cv_generator_node,
    interview_node,
    greeting_node,
    end_node,
)
from career_pilot.graph.edges import route_by_intent
from langsmith import traceable
from langchain_core.messages import HumanMessage


def create_graph() -> StateGraph:
    """Build and compile the LangGraph."""
    graph = StateGraph(AppState)

    graph.add_node("router", router_node)
    graph.add_node("cv_analyzer_node", cv_analyzer_node)
    graph.add_node("job_matcher_node", job_matcher_node)
    graph.add_node("skill_gap_node", skill_gap_node)
    graph.add_node("cv_generator_node", cv_generator_node)
    graph.add_node("interview_node", interview_node)
    graph.add_node("greeting_node", greeting_node)
    graph.add_node("end_node", end_node)

    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "cv_analyzer_node": "cv_analyzer_node",
            "job_matcher_node": "job_matcher_node",
            "skill_gap_node": "skill_gap_node",
            "cv_generator_node": "cv_generator_node",
            "interview_node": "interview_node",
            "greeting_node": "greeting_node",
        },
    )
    graph.add_edge("cv_analyzer_node", "end_node")
    graph.add_edge("job_matcher_node", "end_node")
    graph.add_edge("skill_gap_node", "end_node")
    graph.add_edge("cv_generator_node", "end_node")
    graph.add_edge("interview_node", "end_node")
    graph.add_edge("greeting_node", "end_node")
    graph.add_edge("end_node", END)

    return graph


graph = create_graph().compile()


@traceable
def run_graph(user_message: str, files: list = []) -> str:
    """Run the graph with a user message and optional files."""
    result = graph.invoke(
        {"messages": [HumanMessage(content=user_message)], "files": files}
    )
    return result.get("response", "No response")
