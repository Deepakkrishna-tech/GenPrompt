from jinja2 import Template
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import logging # Use logging here too for consistency

from ..core.schemas import ImagePrompt
from ..core.prompts import IMAGE_PROMPT_ENGINEER_TEMPLATE

logger = logging.getLogger(__name__)

def run_prompt_engineer(state: Dict[str, Any]) -> Dict[str, Any]:
    """Invokes the PromptEngineerAgent to synthesize Prompt A, now with robust error handling."""
    logger.info("---AGENT: PROMPT ENGINEER---")

    # This is the most likely point of failure.
    visual_analysis = state.get('visual_analysis')
    if not visual_analysis:
        logger.error("Visual analysis is missing from the state. Cannot generate prompt.")
        # Return the state unmodified so the app doesn't crash
        return state

    try:
        model = ChatOpenAI(model="gpt-4o", temperature=0.7)
        template = Template(IMAGE_PROMPT_ENGINEER_TEMPLATE)

        # This line can fail if 'visual_analysis' is not the expected object
        prompt_str = template.render(analysis=visual_analysis)
        
        logger.info("Successfully rendered prompt template. Calling OpenAI...")
        response = model.invoke(prompt_str)

        final_prompt = ImagePrompt(prompt_body=response.content)
        
        state['image_prompt'] = final_prompt
        # Ensure prompt_history is initialized before appending
        if 'prompt_history' not in state:
            state['prompt_history'] = []
        state['prompt_history'].append(final_prompt.prompt_body)
        logger.info("Successfully generated and stored new image prompt.")

    except Exception as e:
        logger.error("An error occurred in Prompt Engineer: %s", e, exc_info=True)
        # We don't modify the state, just log the error and let it pass
    
    return state