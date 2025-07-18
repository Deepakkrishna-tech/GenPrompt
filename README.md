# 📡 **GenPrompt: The Creative Co-Pilot**

**GenPrompt** is an AI-first, agent-powered creative tool that transforms static images into high-quality prompts for text-to-image and text-to-video generation. It empowers artists, designers, and storytellers to achieve visual continuity and cinematic quality—not by generating assets directly, but by engineering precise, context-aware prompts using an advanced multimodal system.

![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46-orange.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.5-purple.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 Vision

In generative AI, *great outputs begin with great prompts*. **GenPrompt** acts as your *prompt sommelier*—analyzing the visual DNA of your source image and translating it into rich, stylized instructions for generative models. The goal is creative consistency across modalities, enabling cinematic and brand-aligned storytelling from a single image.

---

## 🚀 Key Features

* **🧠 Two-Stage Workflow**
  Generate a **visual prompt** (Prompt A) from an input image, then extrapolate it into a **cinematic video prompt** (Prompt B) for text-to-video generation.

* **🔍 Deep Visual Analysis**
  Leverages cutting-edge multimodal models (like GPT-4o) to interpret visual tone, artistic style, lighting, subject framing, and more—far beyond simple tagging.

* **🤖 Agent-Based Prompt Engineering**
  Built on **LangGraph** and **LangChain**, GenPrompt uses a team of AI agents—each with a unique persona (visual analyst, prompt engineer, etc.)—to collaboratively deconstruct and reconstruct your creative input into powerful, composable prompts.

* **🗣️ Human-in-the-Loop Iteration**
  A conversational refinement loop lets you review, adjust, and perfect your prompts in real time—ensuring they align with your creative intent before downstream generation.

---

## 🛠️ System Architecture

GenPrompt is built with a decoupled, scalable architecture optimized for flexibility and experimentation.

* **Frontend**:
  Built with **Streamlit** for rapid prototyping and intuitive interaction. Users can upload images, view generated prompts, and provide iterative feedback.

* **Backend**:
  Powered by **FastAPI**, the backend handles asynchronous inference, model orchestration, and agent communication.

* **Agentic Core**:
  At the heart of GenPrompt is a **LangGraph**-orchestrated state machine that routes tasks through specialized agents (e.g., vision analyst → prompt engineer → reviewer), enabling a modular and extensible workflow.

---

## 📦 Tech Stack

| Layer         | Tool/Library                    |
| ------------- | ------------------------------- |
| Frontend      | Streamlit                       |
| Backend       | FastAPI                         |
| Agent System  | LangGraph, LangChain            |
| LLM Backbone  | OpenAI GPT-4o (vision + text)   |
| Prompt Output | JSON (structured for API usage) |

---

## 🧠 Who Is It For?

* **AI Artists & Designers** looking to maintain consistent visual themes across generations.
* **Content Studios** building cinematic sequences with a unified art direction.
* **Researchers & Engineers** interested in building modular, human-in-the-loop creative systems using LangGraph.
* **Product Teams** wanting to augment image/video generation with smarter prompt engineering.

---


