# 📡**GenPrompt** :  **Creative Co-Pilot**

**GenPrompt** is an advanced, agent-based creative tool that transforms static images into dynamic prompts for both AI image and video generation.


![alt text](https://img.shields.io/badge/python-3.12-blue.svg)


![alt text](https://img.shields.io/badge/FastAPI-0.111-green.svg)


![alt text](https://img.shields.io/badge/Streamlit-1.46-orange.svg)


![alt text](https://img.shields.io/badge/LangGraph-0.5-purple.svg)


![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

GenPrompt is an AI-first creative co-pilot that transforms images into high-quality, style-consistent prompts for advanced text-to-image and text-to-video models. It is designed to empower artists, designers, and storytellers to build cinematic or stylized assets with creative continuity—not by generating assets, but by engineering the perfect prompt using an agentic, context-aware system.

🎯 Core Vision

In the world of generative AI, the quality of the output is a direct reflection of the quality of the prompt. GenPrompt acts as a "prompt sommelier," deconstructing the visual DNA of a source image and translating its essence into powerful, model-ready instructions. This ensures creative and stylistic consistency across different generative tasks.

🚀 Key Features

Two-Stage Workflow: A modular pipeline that first generates a detailed image prompt (Prompt A) and then elevates it into a cinematic video direction (Prompt B).

Deep Visual Analysis: Utilizes powerful vision models (like GPT-4o) to go beyond simple keywords, understanding artistic style, mood, lighting, and composition.

Agent-Powered Synthesis: Employs a team of specialized AI agents (built with LangChain and LangGraph) to analyze, engineer, and refine prompts, each with a unique persona and goal.

Iterative Refinement: A built-in human-in-the-loop feedback system allows you to conversationally edit and perfect both image and video prompts until they match your vision.

🛠️ System Architecture

GenPrompt is built on a modern, decoupled architecture to ensure scalability and maintainability.

Frontend: A user-friendly interface built with Streamlit, providing real-time interaction and prompt previews.

Backend: A robust and asynchronous API server built with FastAPI, handling all the heavy computational work.

Agentic Core: An intelligent state machine orchestrated by LangGraph, which routes tasks between specialized AI agents.
