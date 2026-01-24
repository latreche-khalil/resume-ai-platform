"""
API Endpoints Package

Contains all API route handlers for the Resume AI Platform.
"""

from .upload import router as upload_router

__all__ = ['upload_router']
