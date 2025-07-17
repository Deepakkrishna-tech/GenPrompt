# File: src/api/routes.py
# FINAL, SIMPLIFIED VERSION

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import json
import logging # Use logging for errors
from ..core.graph import build_genprompt_graph
from ..core.schemas import AppState, RefineRequest, ImagePrompt
from ..core.schemas import VideoCreativeBrief

router = APIRouter()
graph = build_genprompt_graph()
logger = logging.getLogger(__name__)

@router.post("/invoke-graph", response_model=AppState)
async def invoke_graph_endpoint(image_bytes: UploadFile = File(...), prompt_history_json: str = Form("[]")):
    # ... (no changes needed here)
    try:
        image_data = await image_bytes.read()
        prompt_history = json.loads(prompt_history_json)
        initial_state = AppState(original_image_bytes=image_data, prompt_history=prompt_history)
        result_state = graph.invoke(initial_state.model_dump(exclude_none=True))
        if 'original_image_bytes' in result_state: del result_state['original_image_bytes']
        return result_state
    except Exception as e:
        logger.error("Error in /invoke-graph: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error.")

# --- Corrected Endpoint for Prompt Refinement ---
@router.post("/refine-prompt", response_model=AppState)
async def refine_prompt_endpoint(request: RefineRequest):
    """
    Builds a state containing user feedback and invokes the graph.
    The main graph router will correctly send it to the 'refiner' node.
    """
    try:
        # Construct the state object needed for the refiner agent
        if request.active_prompt_type == "image":
            image_prompt_obj = ImagePrompt(prompt_body=request.prompt_to_refine)
            initial_state = AppState(
                image_prompt=image_prompt_obj,
                user_feedback=request.user_feedback,
                active_prompt_for_refinement=request.active_prompt_type,
                prompt_history=[] # Start with a fresh history for this run
            )
        # --- THIS IS THE FIX ---
        elif request.active_prompt_type == "video":
            initial_state = AppState(
                video_prompt=request.prompt_to_refine,
                user_feedback=request.user_feedback,
                active_prompt_for_refinement=request.active_prompt_type,
                prompt_history=[] # Start with a fresh history for this run
            )
        else:
            # This case should not be reached due to Pydantic validation
            raise HTTPException(status_code=400, detail="Invalid active_prompt_type.")

        # Invoke the graph normally. The new router will handle it.
        result_state = graph.invoke(initial_state.model_dump(exclude_none=True))

        # Clean and return the state
        if 'original_image_bytes' in result_state: del result_state['original_image_bytes']
        if 'generated_image_bytes' in result_state: del result_state['generated_image_bytes']
            
        return result_state

    except Exception as e:
        logger.error("Error in /refine-prompt: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error during refinement.")
    
@router.post("/generate-video-prompt", response_model=AppState)
async def generate_video_prompt_endpoint(
    image_bytes: UploadFile = File(...),
    creative_brief_json: str = Form(...)
):
    """
    Handles the Stage 2 workflow: generating a video prompt from an image
    and a user's creative brief.
    """
    try:
        image_data = await image_bytes.read()
        brief_data = json.loads(creative_brief_json)
        
        # Create a validated VideoCreativeBrief object
        creative_brief = VideoCreativeBrief.model_validate(brief_data)

        # Construct the initial state for the graph.
        # The entry router will see `video_creative_brief` and route correctly.
        initial_state = AppState(
            generated_image_bytes=image_data, # Use the correct key for Stage 2
            video_creative_brief=creative_brief,
            prompt_history=[] # Start with a fresh history
        )

        result_state = graph.invoke(initial_state.model_dump(exclude_none=True))

        # Clean bytes from response
        if 'original_image_bytes' in result_state: del result_state['original_image_bytes']
        if 'generated_image_bytes' in result_state: del result_state['generated_image_bytes']

        return result_state

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for creative_brief.")
    except Exception as e:
        logger.error("Error in /generate-video-prompt: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")