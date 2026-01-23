from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    success: bool
    message: str
    file_id: str
    filename: str
    file_type: str
    file_size: int
    timestamp: str


class AnalysisRequest(BaseModel):
    """Request model for resume analysis"""
    file_id: str = Field(..., description="ID of uploaded file")
    job_description: str = Field(..., description="Target job description text")
