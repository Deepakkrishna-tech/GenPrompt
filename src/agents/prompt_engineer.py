# src/agents/prompt_engineer.py
from jinja2 import Template
from langchain_openai import ChatOpenAI
from typing import Dict, Any

from core.schemas import ImagePrompt
from core.prompts import IMAGE_PROMPT_ENGINEER_TEMPLATE

def run_prompt_engineer(state: Dict[str, Any]) -> Dict[str, Any]:
    """Invokes the PromptEngineerAgent to synthesize Prompt A."""
    print("---AGENT: PROMPT ENGINEER---")

    model = ChatOpenAI(model="gpt-4o", temperature=0.7)
    template = Template(IMAGE_PROMPT_ENGINEER_TEMPLATE)

    prompt_str = template.render(analysis=state['visual_analysis'])
    response = model.invoke(prompt_str)

    final_prompt = ImagePrompt(prompt_body=response.content)
    
    state['image_prompt'] = final_prompt
    if 'prompt_history' not in state:
        state['prompt_history'] = []
    state['prompt_history'].append(final_prompt.prompt_body)
    return state