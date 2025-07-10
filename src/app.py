# src/app.py
import streamlit as st
from dotenv import load_dotenv
from typing import Dict, Any

from core.graph import build_genprompt_graph
from core.schemas import AppState, ImagePrompt, VideoCreativeBrief
# Using the native st.code() for copy functionality.

# --- Page Config & Initialization ---
st.set_page_config(page_title="GenPrompt", layout="wide", page_icon="🎨")
load_dotenv()
@st.cache_resource
def get_graph():
    return build_genprompt_graph()
app_graph = get_graph()

# --- Session State Management ---
if "session_state_dict" not in st.session_state:
    st.session_state.session_state_dict = AppState().model_dump()

# --- Helper Functions ---
def update_state(new_data: Dict[str, Any]):
    st.session_state.session_state_dict.update(new_data)

def invoke_graph(input_data: Dict[str, Any]):
    """Invokes the graph with given data, updates the state, and triggers a rerun."""
    with st.spinner("🚀 GenPrompt agents are working..."):
        result = app_graph.invoke(input_data)
        st.session_state.session_state_dict = result
    # THE FIX: Immediately rerun the script to reflect the new state in the UI.
    st.rerun()

# --- UI Rendering ---
st.title("🎨 GenPrompt")
st.markdown("Your AI Creative Partner for Image and Video Prompts.")

tab1, tab2 = st.tabs(["**Stage 1: Generate Prompt A**", "**Stage 2: Generate Prompt B**"])
current_state_dict = st.session_state.session_state_dict

# === TAB 1: IMAGE TO IMAGE PROMPT (PROMPT A) ===
with tab1:
    st.header("Image → Image Prompt")
    st.caption("Upload your source artwork to generate a new, high-fidelity image prompt.")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        uploaded_file_A = st.file_uploader("Upload your creative starting point...", type=["jpg", "png", "jpeg"], key="uploader_A")
        if uploaded_file_A:
            st.image(uploaded_file_A, caption="Source Image Preview", use_container_width=True)
            if st.button("Generate Image Prompt", use_container_width=True, type="primary", key="button_A"):
                image_bytes = uploaded_file_A.getvalue()
                invoke_graph({"original_image_bytes": image_bytes, "prompt_history": current_state_dict.get("prompt_history", [])})
        
    with col2:
        st.subheader("✅ Prompt A: For Text-to-Image")
        if current_state_dict.get("image_prompt"):
            prompt_obj = ImagePrompt.model_validate(current_state_dict["image_prompt"])
            
            st.write("**Prompt Preview:**")
            with st.container(border=True):
                st.markdown(prompt_obj.prompt_body)
            
            st.write("")
            st.write("**Copyable Prompt & Parameters:**")
            st.code(prompt_obj.prompt_body, language="text")
            st.code(prompt_obj.technical_parameters, language="bash")
            
            with st.form("refine_A_form"):
                st.write("**Refine Prompt A:**")
                refinement_query_A = st.text_input("Enter your changes...", label_visibility="collapsed", key="refine_A_input")
                if st.form_submit_button("Refine", use_container_width=True):
                    if refinement_query_A:
                        update_state({'user_feedback': refinement_query_A, 'active_prompt_for_refinement': "image"})
                        invoke_graph(st.session_state.session_state_dict)
        else:
            st.info("Your generated image prompt will appear here.")

# === TAB 2: IMAGE TO VIDEO PROMPT (PROMPT B) ===
with tab2:
    st.header("Image → Video Prompt")
    st.caption("Upload any image and provide a creative brief to generate a cinematic video direction.")
    col3, col4 = st.columns(2, gap="large")

    with col3:
        with st.form("creative_brief_form"):
            st.subheader("Creative Brief")
            uploaded_file_B = st.file_uploader("1. Upload Image to Animate", type=["jpg", "png", "jpeg"])
            
            moods = st.multiselect(
                "2. Select Moods (Optional)",
                ["Epic & Grandiose", "Tense & Suspenseful", "Dreamy & Surreal", "Fast-Paced & Energetic", "Calm & Serene", "Dark & Mysterious"]
            )
            camera_move = st.selectbox(
                "3. Suggest Camera Movement (Optional)",
                ["(AI Decides)", "Slow Push-In", "Fast Pull-Out", "Tracking Shot (Follow Subject)", "Crane Shot (Up/Down)", "Static / No Movement"]
            )
            notes = st.text_area("4. Additional Notes (Optional)", placeholder="e.g., 'focus on the character's eyes', 'make the rain feel heavy'")
            
            submitted = st.form_submit_button("Generate Video Prompt", use_container_width=True, type="primary")

            if submitted and uploaded_file_B:
                image_bytes_B = uploaded_file_B.getvalue()
                brief = VideoCreativeBrief(
                    moods=moods,
                    camera_movement=camera_move if camera_move != "(AI Decides)" else None,
                    additional_notes=notes
                )
                
                update_state({
                    'generated_image_bytes': image_bytes_B,
                    'video_creative_brief': brief.model_dump()
                })
                invoke_graph(st.session_state.session_state_dict)

        if current_state_dict.get("generated_image_bytes"):
            st.image(current_state_dict["generated_image_bytes"], caption="Image for Video Prompting", use_container_width=True)

    with col4:
        st.subheader("🎬 Prompt B: For Video")
        if current_state_dict.get("video_prompt"):
            video_prompt = current_state_dict["video_prompt"]
            
            st.write("**Video Direction Preview:**")
            with st.container(border=True):
                st.markdown(video_prompt)

            st.write("")
            st.write("**Copyable Video Direction:**")
            st.code(video_prompt, language="text")
            
            with st.form("refine_B_form"):
                st.write("**Refine Prompt B:**")
                refinement_query_B = st.text_input("Enter your changes...", label_visibility="collapsed", key="refine_B_input")
                if st.form_submit_button("Refine", use_container_width=True):
                    if refinement_query_B:
                        update_state({'user_feedback': refinement_query_B, 'active_prompt_for_refinement': "video"})
                        invoke_graph(st.session_state.session_state_dict)
        else:
            st.info("Your generated video prompt will appear here.")