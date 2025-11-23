#!/usr/bin/env python3

import os, sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sources.logger import Logger
from services.interaction_service import get_interaction_service
from routers import query, stream
from config.settings import settings

from dotenv import load_dotenv

load_dotenv()

def is_running_in_docker():
    """Detect if code is running inside a Docker container."""
    if os.path.exists('/.dockerenv'):
        return True
    try:
        with open('/proc/1/cgroup', 'r') as f:
            return 'docker' in f.read()
    except:
        pass
    return False

from middleware.security import api_key_middleware

# Initialize FastAPI
app = FastAPI(title="LAS API", description="Local Agentic System API", version="0.1.0")

# Middleware
app.middleware("http")(api_key_middleware)
logger = Logger("backend.log")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(".screenshots"):
    os.makedirs(".screenshots")
app.mount("/screenshots", StaticFiles(directory=".screenshots"), name="screenshots")

# Initialize Services
try:
    interaction_service = get_interaction_service()
    # Inject interaction service into router (temporary dependency injection)
    query.set_interaction_service(interaction_service)
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    sys.exit(1)

# Include Routers
# Include Routers
app.include_router(query.router)
app.include_router(stream.router)

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    if is_running_in_docker():
        print("[LAS Core] Starting in Docker container...")
    else:
        print("[LAS Core] Starting on host machine...")
    
    envport = os.getenv("BACKEND_PORT")
    port = int(envport) if envport else 7777
    uvicorn.run(app, host="0.0.0.0", port=port)