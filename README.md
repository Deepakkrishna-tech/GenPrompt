# 🎨 **GenPrompt** : Your AI Creative Partner

**GenPrompt** is an advanced, agent-based creative tool that transforms static images into dynamic prompts for both AI image and video generation.

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)](https://streamlit.io)
[![Agent Orchestration](https://img.shields.io/badge/Agents-LangGraph-E86F2C)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

It's designed for artists, designers, and storytellers who want to maintain **creative continuity**—bridging the gap between a single visual idea and a full-fledged cinematic scene. Instead of just generating outputs, GenPrompt provides you with world-class, production-ready prompts to use in your favorite tools like Midjourney, Stable Diffusion, Runway, or Pika.

---

## ✨ Core Features

GenPrompt operates as a modular, two-stage workflow powered by a team of specialized AI agents:

### **Stage 1: Image → Image Prompt (Prompt A)**
Upload any source image and the **VisualAnalystAgent** deconstructs its style, mood, and composition. Then, the **PromptEngineerAgent**, acting as a legendary prompt artist, synthesizes this analysis into a rich, evocative prompt perfect for generating new, high-fidelity images.

*   **Deep Visual Analysis**: Goes beyond keywords to understand artistic intent.
*   **Creative Prompt Synthesis**: Generates prompts that are more artistic and nuanced than simple descriptions.
*   **Iterative Refinement**: A built-in loop allows you to conversationally edit and perfect the prompt with the **RefinerAgent**.

### **Stage 2: Image → Video Prompt (Prompt B)**
This is where the magic of creative continuity happens. You can either:
1.  Upload the image you generated with Prompt A.
2.  Upload any new image to start fresh.

The **VideoDirectorAgent** then steps in.
*   **Context-Aware Direction**: If you use the full workflow, the agent analyzes **both** the original source image and the new image to understand the creative evolution, producing a video prompt that honors the original artistic soul.
*   **AI Collaboration via Creative Brief**: Don't know how to describe camera movements? No problem. A guided "Creative Brief" lets you suggest moods and ideas, and the AI Director elevates them into professional cinematic language.

---

## 🚀 The Agentic Workflow

GenPrompt is built on a sophisticated, conditional graph using **LangGraph**. This allows for a flexible, multi-agent system where different AI specialists collaborate to bring your vision to life.

| Agent                 | Role                                                                        | Core Task                                                   |
| --------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **VisualAnalyst**     | A seasoned Art Director                                                     | Deconstructs an image into structured, artistic insights.   |
| **PromptEngineer**    | A legendary Prompt Artist                                                   | Synthesizes analysis into a masterful text-to-image prompt. |
| **VideoDirector**     | A visionary Film Director                                                   | Translates images and ideas into cinematic video direction. |
| **Refiner**           | A master Prompt Editor                                                      | Seamlessly integrates user feedback into any prompt.        |

---

## 🛠️ Tech Stack

This project is built with a modern, 2025-ready open-source stack:

*   **Frontend**: [Streamlit](https://streamlit.io/)
*   **Agent Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph)
*   **LLM Integration**: [LangChain](https://www.langchain.com/) (using GPT-4o)
*   **Prompt Templating**: [Jinja2](https://jinja.palletsprojects.com/)
*   **Data Validation**: [Pydantic](https://pydantic.dev/)
*   **Dependency Management**: [Poetry](https://python-poetry.org/)


🗺️ Future Roadmap

Style Memory: Allow users to save and reuse preferred aesthetic profiles.

Direct API Integration: One-click generation by connecting directly to image/video APIs like Fal.ai or Replicate.

Visual Feedback Loop: Use CLIP or other vision models to score the alignment of generated prompts.

Advanced Prompt History: Save, search, and tag your favorite prompts in a persistent database like ChromaDB.
