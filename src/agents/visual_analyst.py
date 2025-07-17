# File: src/agents/visual_analyst.py

import base64
import logging
from typing import Dict, Any

from ..config import settings
from ..core.schemas import VisualAnalysis
from ..core.prompts import VISUAL_ANALYST_TEMPLATE

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

def encode_image_to_base64(image_bytes: bytes) -> str:
    """
    Encodes raw image bytes into a base64 JPEG string for OpenAI Vision API.
    """
    try:
        return base64.b64encode(image_bytes).decode("utf-8")
    except Exception as e:
        logger.error("[Encoding Error] Failed to encode image: %s", e)
        raise

def build_vision_message(encoded_image: str) -> HumanMessage:
    """
    Constructs a multimodal prompt message combining instruction and image.
    """
    return HumanMessage(content=[
        {"type": "text", "text": VISUAL_ANALYST_TEMPLATE},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
    ])

def initialize_gpt4o_parser() -> ChatOpenAI:
    """
    Initializes the GPT-4o model with structured output parsing.
    """
    return ChatOpenAI(
        model=settings.PARSER_LLM_ID,
        api_key=settings.OPENAI_API_KEY,
        temperature=0.1,
        max_retries=2,
        request_timeout=60
    ).with_structured_output(VisualAnalysis)

def fallback_analysis(error: Exception) -> VisualAnalysis:
    """
    Creates a fallback object in case the visual analysis fails.
    """
    return VisualAnalysis(
        main_subject="Analysis failed",
        setting_and_environment="Unknown",
        artistic_style="Unknown",
        mood_and_atmosphere="Unknown",
        lighting_style="Unknown",
        color_scheme=["Unknown"],
        compositional_notes=f"Error during analysis: {error}"
    )

def run_visual_analyst(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function to analyze an image using GPT-4o Vision
    and inject structured visual metadata into the graph state.
    """
    logger.info("[Node] 🎬 Running GPT-4o Visual Analyst...")

    image_bytes = state.get("original_image_bytes")
    if not isinstance(image_bytes, bytes):
        logger.error("[Error] `original_image_bytes` is missing or invalid in the state.")
        raise ValueError("Missing or invalid `original_image_bytes` in state.")

    try:
        encoded_image = encode_image_to_base64(image_bytes)
        message = build_vision_message(encoded_image)
        model = initialize_gpt4o_parser()
        
        # Perform analysis
        structured_analysis = model.invoke([message])
        logger.info("[Node] ✅ Visual analysis successful.")

    except Exception as e:
        logger.error("[Fatal Error] GPT-4o visual analysis failed: %s", e, exc_info=True)
        structured_analysis = fallback_analysis(e)

    # Update state and return
    state["visual_analysis"] = structured_analysis
    return state
