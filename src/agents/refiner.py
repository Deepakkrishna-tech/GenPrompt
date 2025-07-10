# src/agents/refiner.py
from jinja2 import Template
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Literal

from core.prompts import PROMPT_REFINER_TEMPLATE
from core.schemas import ImagePrompt

def run_refiner(state: Dict[str, Any]) -> Dict[str, Any]:
    """Invokes the generic RefinementAgent to edit a prompt based on user feedback."""
    print("---AGENT: REFINER---")

    model = ChatOpenAI(model="gpt-4o", temperature=0.7)
    template = Template(PROMPT_REFINER_TEMPLATE)

    active_prompt_type: Literal["image", "video"] = state.get("active_prompt_for_refinement")
    prompt_to_refine = ""

    if active_prompt_type == "video" and state.get("video_prompt"):
        prompt_to_refine = state["video_prompt"]
    elif active_prompt_type == "image" and state.get("image_prompt"):
        # ImagePrompt is a Pydantic model, so we access its attribute
        prompt_to_refine = state["image_prompt"].prompt_body
    
    if not prompt_to_refine:
        # Failsafe if the state is not set correctly
        state['user_feedback'] = None # Clear feedback to prevent loop
        return state

    prompt_str = template.render(
        original_prompt=prompt_to_refine,
        user_feedback=state['user_feedback']
    )
    
    response = model.invoke(prompt_str)
    refined_prompt = response.content

    # Update the correct prompt in the state
    if active_prompt_type == "video":
        state["video_prompt"] = refined_prompt
    elif active_prompt_type == "image":
        # We need to recreate the Pydantic object
        current_params = state["image_prompt"].technical_parameters
        state["image_prompt"] = ImagePrompt(prompt_body=refined_prompt, technical_parameters=current_params)
    
    state['prompt_history'].append(refined_prompt)
    # CRITICAL: Clear the user feedback to prevent an infinite loop.
    state['user_feedback'] = None

    return state