# src/core/graph.py

from langgraph.graph import StateGraph, END
from typing import Literal, Dict, Any

# Import the agent runners
from agents.visual_analyst import run_visual_analyst
from agents.prompt_engineer import run_prompt_engineer
from agents.video_director import run_video_director
from agents.refiner import run_refiner

def entry_point_router(state: Dict[str, Any]) -> Literal["visual_analyst_for_prompt_a", "visual_analyst_for_prompt_b"]:
    """Determines the starting point of the graph based on the initial input."""
    print("---ROUTING ENTRY POINT---")
    # If we have 'generated_image_bytes', it means the user started at Stage 2.
    if state.get("generated_image_bytes"):
        print("Entry Point: Stage 2 (Video Prompt)")
        return "visual_analyst_for_prompt_b"
    else:
        print("Entry Point: Stage 1 (Image Prompt)")
        return "visual_analyst_for_prompt_a"

def decide_next_step(state: Dict[str, Any]) -> Literal["refine", "direct_video", "end"]:
    """Determines the next step based on the current application state."""
    print("---DECISION POINT---")
    
    if state.get("user_feedback"):
        print("Routing to: REFINE")
        return "refine"
    
    # This condition is for the Stage 1 to Stage 2 transition
    if state.get("generated_image_bytes") and not state.get("video_prompt"):
        print("Routing to: VIDEO DIRECTOR")
        return "direct_video"

    print("Routing to: END")
    return "end"

def build_genprompt_graph():
    """Builds the complete, conditional LangGraph for the GenPrompt application."""
    workflow = StateGraph(Dict[str, Any])

    # === Add all agents as nodes in the graph ===
    workflow.add_node("visual_analyst_for_prompt_a", run_visual_analyst)
    workflow.add_node("visual_analyst_for_prompt_b", run_visual_analyst) # Same function, different node name for routing
    workflow.add_node("prompt_engineer", run_prompt_engineer)
    workflow.add_node("video_director", run_video_director)
    workflow.add_node("refiner", run_refiner)

    # === Define the graph's control flow (edges) ===
    workflow.set_conditional_entry_point(
        entry_point_router,
        {
            "visual_analyst_for_prompt_a": "visual_analyst_for_prompt_a",
            "visual_analyst_for_prompt_b": "visual_analyst_for_prompt_b",
        }
    )

    # Path for Stage 1
    workflow.add_edge("visual_analyst_for_prompt_a", "prompt_engineer")

    # Path for Stage 2 (when started directly)
    # After analyzing the image, go straight to the video director
    workflow.add_edge("visual_analyst_for_prompt_b", "video_director")

    # Edges from the decision points
    workflow.add_conditional_edges("prompt_engineer", decide_next_step, {"refine": "refiner", "direct_video": "video_director", "end": END})
    workflow.add_conditional_edges("video_director", decide_next_step, {"refine": "refiner", "end": END})
    workflow.add_conditional_edges("refiner", decide_next_step, {"refine": "refiner", "direct_video": "video_director", "end": END})

    app = workflow.compile()
    return app