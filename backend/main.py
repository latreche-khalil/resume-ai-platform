"""
Resume AI Platform - Main Application

FastAPI backend for AI-powered resume analysis with OCR support.
"""

import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints.upload import router as upload_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Resume AI Platform",
    description="AI-powered resume analysis with explainable feedback",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(upload_router)


@app.get("/", tags=["info"])
async def root():
    """API information endpoint."""
    return {
        "name": "Resume AI Platform API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "upload": "/api/upload",
            "extract": "/api/extract/{file_id}",
            "health": "/health"
        }
    }


@app.get("/health", tags=["monitoring"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "resume-ai-backend"
    }


@app.on_event("startup")
async def startup():
    """Application startup handler."""
    logger.info(" Resume AI Backend Started")
    logger.info(" API Docs: http://localhost:8000/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
