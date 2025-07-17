# File: src/core/graph.py
# FINAL, CORRECTED VERSION. The router is now aware of refinement.

from langgraph.graph import StateGraph, END
from typing import Dict, Any, Literal

# Import all agent runners
from ..agents.visual_analyst import run_visual_analyst
from ..agents.prompt_engineer import run_prompt_engineer
from ..agents.video_director import run_video_director
from ..agents.refiner import run_refiner

def entry_or_refine_router(state: Dict[str, Any]) -> Literal["visual_analyst", "refiner", "video_director"]:
    """
    This is the main router. It decides if this is a new job or a refinement job.
    """
    print("---MAIN ROUTER---")
    # If there is user feedback, we ALWAYS go to the refiner first.
    if state.get("user_feedback"):
        print("Routing to: REFINE")
        return "refiner"
    
    # Otherwise, it's a new job. Decide between Stage 1 or Stage 2.
    if state.get("video_creative_brief") is not None:
        print("Routing to: VIDEO DIRECTOR")
        return "video_director"
    else:
        print("Routing to: VISUAL ANALYST")
        return "visual_analyst"


def build_genprompt_graph():
    """Builds the complete, conditional LangGraph for the GenPrompt application."""
    workflow = StateGraph(Dict[str, Any])

    # Add all agent nodes
    workflow.add_node("visual_analyst", run_visual_analyst)
    workflow.add_node("prompt_engineer", run_prompt_engineer)
    workflow.add_node("video_director", run_video_director)
    workflow.add_node("refiner", run_refiner)

    # --- Corrected Graph Wiring ---
    
    # 1. Use the new, smarter conditional entry point.
    workflow.set_conditional_entry_point(
        entry_or_refine_router,
        {
            "visual_analyst": "visual_analyst",
            "video_director": "video_director",
            "refiner": "refiner", # Add the mapping for the refiner path
        }
    )

    # 2. Define the paths from each node.
    workflow.add_edge("visual_analyst", "prompt_engineer")
    workflow.add_edge("prompt_engineer", END) # Stage 1 ends after prompt engineering
    workflow.add_edge("video_director", END)  # Stage 2 ends after video direction
    workflow.add_edge("refiner", END)         # Refinement ends after refining

    app = workflow.compile()
    print("✅ GenPrompt Graph Compiled with FINAL, CORRECTED logic.")
    return app