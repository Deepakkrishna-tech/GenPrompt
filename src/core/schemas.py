# src/core/schemas.py
# This is the complete and correct schema definition for the GenPrompt application.
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

# DEFINITION for the user's creative input in Stage 2
class VideoCreativeBrief(BaseModel):
    """A structured brief from the user to guide the VideoDirectorAgent."""
    moods: Optional[List[str]] = Field(default=None, description="Suggested moods, e.g., 'Tense', 'Dreamy'.")
    camera_movement: Optional[str] = Field(default=None, description="A preferred camera movement.")
    additional_notes: Optional[str] = Field(default=None, description="Any other free-text ideas from the user.")

# RESTORED: The essential definition for the Visual Analyst's output
class VisualAnalysis(BaseModel):
    """Structured analysis from the VisualAnalystAgent, tailored for artistic and cinematic interpretation."""
    main_subject: str = Field(..., description="The primary subject(s) of the image, including their actions or state.")
    setting_and_environment: str = Field(..., description="The background, environment, and context of the scene.")
    artistic_style: str = Field(..., description="e.g., 'Hyperrealistic digital painting', 'Surrealist oil on canvas', 'Gritty cyberpunk anime'.")
    mood_and_atmosphere: str = Field(..., description="The emotional tone and feeling, e.g., 'Somber and melancholic', 'Epic and awe-inspiring'.")
    lighting_style: str = Field(..., description="e.g., 'Dramatic Rembrandt lighting', 'Soft, diffused morning light', 'Neon-drenched cityscape'.")
    color_scheme: List[str] = Field(..., description="Key colors and their interplay, e.g., ['deep crimson', 'gold accents', 'cool grey undertones'].")
    compositional_notes: str = Field(..., description="Notes on framing, perspective, and depth, e.g., 'Low-angle shot, rule of thirds'.")

# DEFINITION for the output of Stage 1
class ImagePrompt(BaseModel):
    """The structured T2I prompt (Prompt A)."""
    prompt_body: str = Field(..., description="The main, descriptive part of the prompt.")
    technical_parameters: str = Field(default="--ar 16:9 --v 6.0 --style raw", description="Suggested parameters for models like Midjourney.")

# The complete state object for the entire application
class AppState(BaseModel):
    """The complete, stateful 'story' of a user's session. It holds all data."""
    original_image_bytes: Optional[bytes] = None
    generated_image_bytes: Optional[bytes] = None
    visual_analysis: Optional[VisualAnalysis] = None
    video_creative_brief: Optional[VideoCreativeBrief] = None
    image_prompt: Optional[ImagePrompt] = None
    video_prompt: Optional[str] = None
    user_feedback: Optional[str] = None
    prompt_history: List[str] = []
    active_prompt_for_refinement: Optional[Literal["image", "video"]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)