# File: src/app.py
# FINAL VERSION: Contains the fully functional refinement form logic.

import streamlit as st
from dotenv import load_dotenv
import requests
import json
from typing import Dict, Any

from .core.schemas import AppState, ImagePrompt

def main():
    """The main function that runs the Streamlit UI."""
    st.set_page_config(page_title="GenPrompt", layout="wide", page_icon="🎨")
    load_dotenv()

    BACKEND_URL = "http://127.0.0.1:8000/api"

    if "session_state_dict" not in st.session_state:
        st.session_state.session_state_dict = AppState().model_dump()

    # This function is correct. No changes needed.
    def invoke_backend_graph(uploaded_file):
        # ... (Your existing invoke_backend_graph function)
        with st.spinner("🚀 GenPrompt agents are working on the backend..."):
            try:
                files = {'image_bytes': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                prompt_history = st.session_state.session_state_dict.get("prompt_history", [])
                data = {'prompt_history_json': json.dumps(prompt_history)}

                response = requests.post(f"{BACKEND_URL}/invoke-graph", files=files, data=data)
                response.raise_for_status()
                st.session_state.session_state_dict = response.json()
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {e}")

    # --- UI Rendering ---
    st.title("🎨 GenPrompt")
    st.markdown("Your AI Creative Partner for Image and Video Prompts.")

    tab1, tab2 = st.tabs(["**Stage 1: Generate Prompt A**", "**Stage 2: Generate Prompt B**"])
    current_state_dict = st.session_state.session_state_dict

    with tab1:
        st.header("Image → Image Prompt")
        col1, col2 = st.columns(2, gap="large")

        with col1:
            # This part is correct. No changes needed.
            uploaded_file_A = st.file_uploader("Upload your creative starting point...", type=["jpg", "png", "jpeg"], key="uploader_A")
            if uploaded_file_A:
                st.image(uploaded_file_A, caption="Source Image Preview", use_container_width=True)
            if st.button("Generate Image Prompt", use_container_width=True, type="primary", key="button_A"):
                if uploaded_file_A:
                    invoke_backend_graph(uploaded_file_A)
                else:
                    st.warning("Please upload a file first.")
                    
        with col2:
            st.subheader("✅ Prompt A: Text-to-Image")
            if current_state_dict.get("image_prompt"):
                prompt_obj = ImagePrompt.model_validate(current_state_dict["image_prompt"])
                st.write("**Prompt Preview:**")
                with st.container(border=True):
                    st.markdown(prompt_obj.prompt_body)
                st.write("")
                st.write("**Copyable Prompt & Parameters:**")
                st.code(prompt_obj.prompt_body, language="text")
                st.code(prompt_obj.technical_parameters, language="bash")
                
                # === THIS IS THE CORRECTED REFINEMENT FORM ===
                with st.form("refine_A_form"):
                    st.write("**Refine Prompt A:**")
                    refinement_query_A = st.text_input(
                        "Enter your changes (e.g., 'make it darker', 'add a dragon')", 
                        label_visibility="collapsed", 
                        key="refine_A_input"
                    )
                    if st.form_submit_button("Refine", use_container_width=True):
                        if refinement_query_A:
                            with st.spinner("🧠 Refining prompt..."):
                                payload = {
                                    "active_prompt_type": "image",
                                    "prompt_to_refine": prompt_obj.prompt_body,
                                    "user_feedback": refinement_query_A
                                }
                                try:
                                    response = requests.post(f"{BACKEND_URL}/refine-prompt", json=payload)
                                    response.raise_for_status()
                                    # Update state and rerun to display the new prompt
                                    st.session_state.session_state_dict = response.json()
                                    st.rerun()
                                except requests.exceptions.RequestException as e:
                                    st.error(f"API Error during refinement: {e}")
            else:
                st.info("Your generated image prompt will appear here.")
    
    # File: src/app.py (replace the entire "with tab2:" block)

    with tab2:
        st.header("Image → Video Prompt")
        st.caption("Upload any image and provide a creative brief to generate a cinematic video direction.")
        col3, col4 = st.columns(2, gap="large")

        with col3:
            # Step 1: Handle the file upload separately
            uploaded_file_B = st.file_uploader("1. Upload Image to Animate", type=["jpg", "png", "jpeg"], key="uploader_B")

            # Step 2: If a file is uploaded, show its preview immediately
            if uploaded_file_B:
                st.image(uploaded_file_B, caption="Image to Animate Preview", use_container_width=True)

            # Step 3: The form for the creative brief
            with st.form("creative_brief_form"):
                st.subheader("Creative Brief")
                
                moods = st.multiselect(
                    "2. Select Moods (Optional)",
                    ["Epic & Grandiose", "Tense & Suspenseful", "Dreamy & Surreal", "Fast-Paced & Energetic", "Calm & Serene", "Dark & Mysterious"]
                )
                camera_move = st.selectbox(
                    "3. Suggest Camera Movement (Optional)",
                    ["(AI Decides)", "Slow Push-In", "Fast Pull-Out", "Tracking Shot (Follow Subject)", "Crane Shot (Up/Down)", "Static / No Movement"]
                )
                notes = st.text_area("4. Additional Notes (Optional)", placeholder="e.g., 'focus on the character's eyes', 'make the rain feel heavy'")
                
                # --- THIS IS THE CORRECTED LOGIC ---
                submitted = st.form_submit_button("Generate Video Prompt", use_container_width=True, type="primary")
                if submitted:
                    # We check for the uploaded file *inside* the form submission logic
                    if uploaded_file_B is None:
                        st.warning("Please upload an image to animate before generating.")
                    else:
                        # If we have a file, proceed with the API call
                        with st.spinner("🎬 The Video Director is on set..."):
                            from .core.schemas import VideoCreativeBrief
                            
                            brief = VideoCreativeBrief(
                                moods=moods if moods else None,
                                camera_movement=camera_move if camera_move != "(AI Decides)" else None,
                                additional_notes=notes if notes else None,
                            )
                            
                            files = {'image_bytes': (uploaded_file_B.name, uploaded_file_B.getvalue(), uploaded_file_B.type)}
                            data = {'creative_brief_json': brief.model_dump_json()}
                            
                            try:
                                response = requests.post(f"{BACKEND_URL}/generate-video-prompt", files=files, data=data)
                                response.raise_for_status()
                                # Update state and trigger the final rerun to display the output
                                st.session_state.session_state_dict = response.json()
                                st.rerun()
                            except requests.exceptions.RequestException as e:
                                st.error(f"API Error during video prompt generation: {e}")

        # File: src/app.py (replace the "with col4:" block)

        with col4:
            st.subheader("🎬 Prompt B: For Video")
            if current_state_dict.get("video_prompt"):
                # The video_prompt is just a string, so we can use it directly
                video_prompt = current_state_dict["video_prompt"]
                
                st.write("**Video Direction Preview:**")
                with st.container(border=True):
                    st.markdown(video_prompt)
                st.write("")
                st.write("**Copyable Video Direction:**")
                st.code(video_prompt, language="text")

                # === THIS IS THE NEW, FUNCTIONAL REFINEMENT FORM FOR PROMPT B ===
                with st.form("refine_B_form"):
                    st.write("**Refine Prompt B:**")
                    refinement_query_B = st.text_input(
                        "Enter your changes (e.g., 'make it slower', 'add a rain effect')",
                        label_visibility="collapsed",
                        key="refine_B_input"
                    )
                    if st.form_submit_button("Refine", use_container_width=True):
                        if refinement_query_B:
                            with st.spinner("🧠 Refining video direction..."):
                                # This payload is almost identical to the Stage 1 version,
                                # but with active_prompt_type set to "video".
                                payload = {
                                    "active_prompt_type": "video",
                                    "prompt_to_refine": video_prompt,
                                    "user_feedback": refinement_query_B
                                }
                                try:
                                    response = requests.post(f"{BACKEND_URL}/refine-prompt", json=payload)
                                    response.raise_for_status()
                                    # Update state and rerun to display the new refined prompt
                                    st.session_state.session_state_dict = response.json()
                                    st.rerun()
                                except requests.exceptions.RequestException as e:
                                    st.error(f"API Error during refinement: {e}")
            else:
                st.info("Your generated video prompt will appear here.")