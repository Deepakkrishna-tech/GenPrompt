# src/agents/visual_analyst.py
import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, Any

from core.schemas import VisualAnalysis
from core.prompts import VISUAL_ANALYST_TEMPLATE

def run_visual_analyst(state: Dict[str, Any]) -> Dict[str, Any]:
    """Invokes the VisualAnalystAgent to deconstruct the user's image."""
    print("---AGENT: VISUAL ANALYST---")

    model = ChatOpenAI(model="gpt-4o", temperature=0.1)
    structured_llm = model.with_structured_output(VisualAnalysis)

    encoded_image = base64.b64encode(state['original_image_bytes']).decode('utf-8')

    message = HumanMessage(
        content=[
            {"type": "text", "text": VISUAL_ANALYST_TEMPLATE},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
        ]
    )
    analysis = structured_llm.invoke([message])
    state['visual_analysis'] = analysis
    return state