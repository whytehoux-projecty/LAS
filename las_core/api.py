#!/usr/bin/env python3

import os, sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sources.logger import Logger
from services.interaction_service import get_interaction_service
from routers import query, stream, models, preferences, ollama_admin
from config.settings import settings

# Initialize database
from database.models import init_db
init_db()

app = FastAPI(title="LAS API", description="Local Agentic System API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup security middleware (headers + rate limiting)
from middleware.security_middleware import setup_security_middleware
setup_security_middleware(app)

# Include Routers - Legacy (backward compatibility - will be deprecated)
app.include_router(query.router, prefix="/api", tags=["query-legacy"])
app.include_router(stream.router, prefix="/api", tags=["stream-legacy"])
app.include_router(models.router, prefix="/api", tags=["models-legacy"])

# Create v1 API router
from fastapi import APIRouter
v1_router = APIRouter(prefix="/v1")

# Include all routers under v1
v1_router.include_router(query.router, tags=["query"])
v1_router.include_router(stream.router, tags=["stream"])
v1_router.include_router(models.router, tags=["models"])
v1_router.include_router(preferences.router, tags=["preferences"])
v1_router.include_router(ollama_admin.router, tags=["ollama"])

# Import and register authentication router (high priority)
from routers import auth
v1_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Import and register memory router
from routers import memory
v1_router.include_router(memory.router, prefix="/memory", tags=["memory"])

# Import and register voice/multimodal router
from routers import voice
v1_router.include_router(voice.router, prefix="/voice", tags=["voice", "multimodal"])

# Import and register plugins router
from routers import plugins
v1_router.include_router(plugins.router, prefix="/plugins", tags=["plugins"])

# Import and register MCP inspector router
from routers import mcp_inspector
v1_router.include_router(mcp_inspector.router, prefix="/mcp", tags=["mcp"])

# Import and register webhooks router
from routers import webhooks
v1_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])

# Import and register performance router
from routers import performance
v1_router.include_router(performance.router, prefix="/perf", tags=["performance"])

# Import and register security router
from routers import security
v1_router.include_router(security.router, prefix="/security", tags=["security"])

# Import and register workflows router
from routers import workflows
v1_router.include_router(workflows.router, tags=["workflows"])

# Import and register HuggingFace router
from routers import huggingface
v1_router.include_router(huggingface.router, tags=["huggingface", "ai-models"])

# Mount v1 router under /api
app.include_router(v1_router, prefix="/api")

# Keep legacy routes for backward compatibility (deprecated - remove in 12 weeks)
# Note: These provide temporary backward compatibility alongside v1

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "version": "0.1.0", "api_version": "v1"}

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    """Generate custom OpenAPI schema with enhanced documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="LAS API - Local Agent System",
        version="1.0.0",
        description="""
        # Local Agent System (LAS) API
        
        A comprehensive API for AI-powered agent interactions, workflow management, and multi-provider LLM integration.
        
        ## Features
        - 🔐 **JWT Authentication** with role-based access control
        - 🤖 **8 LLM Providers** (OpenAI, Claude, Gemini, Groq, etc.)
        - 📝 **Workflow Builder** for complex agent tasks
        - 🧠 **Memory Management** with knowledge graphs
        - 🔌 **Plugin System** for extensibility
        - ⚡ **Performance Optimized** with Redis caching & connection pooling
        
        ## Authentication
        
        Most endpoints require JWT authentication. To authenticate:
        
        1. Register: `POST /api/v1/auth/register`
        2. Login: `POST /api/v1/auth/login` → Get `access_token`
        3. Use token: Add header `Authorization: Bearer {access_token}`
        
        ## Rate Limiting
        
        - **Auth endpoints**: 5 requests/minute
        - **Query endpoints**: 60 requests/minute  
        - **Default**: 100 requests/minute
        
        ## API Versioning
        
        All endpoints are versioned under `/api/v1/`. Legacy `/api/` routes are deprecated.
        """,
        routes=app.routes,
        contact={
            "name": "LAS Support",
            "email": "support@las.local",
        },
        license_info={
            "name": "MIT",
        }
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from `/api/v1/auth/login`"
        }
    }
    
    # Add tags for organization
    openapi_schema["tags"] = [
        {"name": "Authentication", "description": "User authentication and authorization"},
        {"name": "Query", "description": "LLM query and response endpoints"},
        {"name": "Providers", "description": "LLM provider management"},
        {"name": "Memory", "description": "Knowledge graph and skill management"},
        {"name": "Workflows", "description": "Workflow creation and execution"},
        {"name": "Plugins", "description": "Plugin discovery and management"},
        {"name": "Performance", "description": "Performance monitoring and caching"},
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    if is_running_in_docker():
        print("[LAS Core] Starting in Docker container...")
    else:
        print("[LAS Core] Starting on host machine...")
    
    envport = os.getenv("BACKEND_PORT")
    port = int(envport) if envport else 7777
    uvicorn.run(app, host="0.0.0.0", port=port)