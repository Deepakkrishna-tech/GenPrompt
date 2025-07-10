# src/agents/video_director.py
import base64
from jinja2 import Template
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, Any, List

from core.prompts import VIDEO_DIRECTOR_TEMPLATE
from core.schemas import VideoCreativeBrief # Import the new schema

def run_video_director(state: Dict[str, Any]) -> Dict[str, Any]:
    """Invokes the VideoDirectorAgent, using a user's creative brief if available."""
    print("---AGENT: VIDEO DIRECTOR---")
    
    model = ChatOpenAI(model="gpt-4o", temperature=0.8)
    template = Template(VIDEO_DIRECTOR_TEMPLATE)
    
    # We always need an image for the video director to work on.
    # This image could be from stage 1-2 flow, or a direct upload to stage 2.
    image_to_animate = state.get("generated_image_bytes")
    if not image_to_animate:
        print("Error: Video director called without an image to animate.")
        return state

    # Check for the creative brief
    creative_brief_data = state.get("video_creative_brief")
    creative_brief = VideoCreativeBrief.model_validate(creative_brief_data) if creative_brief_data else None

    # Prepare the prompt and the message payload
    prompt_str = template.render(creative_brief=creative_brief)
    message_content: List[Dict[str, Any]] = [{"type": "text", "text": prompt_str}]
    
    encoded_image = base64.b64encode(image_to_animate).decode('utf-8')
    message_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}})

    # Invoke the model
    message = HumanMessage(content=message_content)
    response = model.invoke([message])
    
    # Update state
    state['video_prompt'] = response.content
    state['prompt_history'].append(response.content)
    # Clear fields that triggered this path to prevent loops
    state['video_creative_brief'] = None
    state['user_feedback'] = None
    
    return state