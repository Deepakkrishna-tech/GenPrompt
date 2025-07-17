# File: src/agents/video_director.py
# FINAL, CORRECTED VERSION with the NameError fixed.

import base64
import logging
from jinja2 import Template
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, Any, List

from ..core.prompts import VIDEO_DIRECTOR_TEMPLATE
from ..core.schemas import VideoCreativeBrief

logger = logging.getLogger(__name__)

def run_video_director(state: Dict[str, Any]) -> Dict[str, Any]:
    """Invokes the VideoDirectorAgent, using a user's creative brief if available."""
    logger.info("---AGENT: VIDEO DIRECTOR---")
    
    try:
        # --- THIS IS THE FIX ---
        # The ChatOpenAI instance must be assigned to the 'model' variable.
        model = ChatOpenAI(model="gpt-4o", temperature=0.8)
        template = Template(VIDEO_DIRECTOR_TEMPLATE)
        
        image_to_animate = state.get("generated_image_bytes")
        if not image_to_animate:
            logger.error("Video director called without an image to animate.")
            return state

        creative_brief = None
        if state.get("video_creative_brief"):
            creative_brief = VideoCreativeBrief.model_validate(state["video_creative_brief"])

        prompt_str = template.render(creative_brief=creative_brief)
        message_content: List[Dict[str, Any]] = [{"type": "text", "text": prompt_str}]
        
        encoded_image = base64.b64encode(image_to_animate).decode('utf-8')
        message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})

        logger.info("Generating video direction...")
        message = HumanMessage(content=message_content)
        
        # This line will now work because the 'model' variable exists.
        response = model.invoke([message])
        logger.info("Successfully generated video direction.")
        
        state['video_prompt'] = response.content.strip()
        if 'prompt_history' not in state:
            state['prompt_history'] = []
        state['prompt_history'].append(response.content.strip())
        
    except Exception as e:
        logger.error("An error occurred in Video Director agent: %s", e, exc_info=True)
    
    finally:
        state['video_creative_brief'] = None
        state['user_feedback'] = None
    
    return state