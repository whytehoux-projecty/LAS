from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from config.settings import settings
import os

# Simple API Key security
# In production, this should be more robust (e.g., JWT, OAuth2)

async def api_key_middleware(request: Request, call_next):
    # Skip security for health check and docs
    if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)
    
    # Allow OPTIONS requests for CORS
    if request.method == "OPTIONS":
        return await call_next(request)

    # Check for API Key if configured
    api_key = os.getenv("LAS_API_KEY")
    if api_key:
        request_key = request.headers.get("X-API-Key")
        if not request_key or request_key != api_key:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or missing API Key"}
            )
            
    response = await call_next(request)
    return response
