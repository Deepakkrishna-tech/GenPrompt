# File: src/agents/refiner.py
# FINAL, HARDENED VERSION

import logging
from typing import Dict, Any
from jinja2 import Template
from langchain_openai import ChatOpenAI

from ..core.schemas import ImagePrompt
from ..core.prompts import PROMPT_REFINER_TEMPLATE

logger = logging.getLogger(__name__)

def run_refiner(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Refines an existing prompt based on user feedback, with robust error handling.
    """
    logger.info("---AGENT: REFINER---")

    feedback = state.get("user_feedback")
    active_prompt_type = state.get("active_prompt_for_refinement")
    
    if not feedback or not active_prompt_type:
        logger.warning("Refiner called without feedback or active prompt type. Skipping.")
        return state

    try:
        prompt_to_refine = ""
        # Safely get the prompt body, whether it's from a Pydantic model or a dict
        if active_prompt_type == "image":
            image_prompt_data = state.get("image_prompt", {})
            prompt_to_refine = image_prompt_data.get("prompt_body")
        elif active_prompt_type == "video":
            prompt_to_refine = state.get("video_prompt")

        if not prompt_to_refine:
            logger.error(f"Could not find prompt to refine for type: {active_prompt_type}")
            state['user_feedback'] = None # Clear feedback to prevent loop
            return state

        # Initialize model and template
        model = ChatOpenAI(model="gpt-4o", temperature=0.5)
        template = Template(PROMPT_REFINER_TEMPLATE)

        refiner_prompt_str = template.render(
            original_prompt=prompt_to_refine,
            user_feedback=feedback
        )
        
        logger.info("Refining prompt...")
        response = model.invoke(refiner_prompt_str)
        refined_prompt_body = response.content.strip()

        # Update the state correctly
        if active_prompt_type == "image":
            # Reconstruct the ImagePrompt object to maintain schema consistency
            state['image_prompt'] = ImagePrompt(prompt_body=refined_prompt_body)
            logger.info("Successfully refined image prompt.")
        else:
            state['video_prompt'] = refined_prompt_body
            logger.info("Successfully refined video prompt.")
        
        # Ensure prompt_history list exists before appending
        if 'prompt_history' not in state:
            state['prompt_history'] = []
        state['prompt_history'].append(refined_prompt_body)

    except Exception as e:
        logger.error("An error occurred in the Refiner agent: %s", e, exc_info=True)

    # CRITICAL: Always clear feedback to prevent an infinite loop.
    state['user_feedback'] = None
    return state