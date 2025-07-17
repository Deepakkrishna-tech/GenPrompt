# File: src/main.py
# FINAL VERSION with logging configured.

import logging
import os
from fastapi import FastAPI
from dotenv import load_dotenv

# --- RECOMMENDED CHANGE: CONFIGURE LOGGING ---
# This setup ensures that all log messages at the INFO level and above
# from all modules (like visual_analyst) will be displayed in your terminal.
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
)

# --- Your existing code (with one import path fix) ---
from .api import routes  # Use a relative import for robustness

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="GenPrompt API",
    version="1.0.0",
    description="Backend services for the GenPrompt creative co-pilot.",
)

# All routes defined in `.api.routes` will be prefixed with `/api`
app.include_router(routes.router, prefix="/api")

@app.get("/", tags=["Health Check"])
async def read_root():
    """Health check endpoint to confirm the API is running."""
    return {"status": "GenPrompt API is running"}