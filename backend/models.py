"""
Pydantic Models for Resume AI Platform

Data models for API request/response validation.
"""

from pydantic import BaseModel, Field


class FileUploadResponse(BaseModel):
    """Response model for file upload endpoint."""
    success: bool
    message: str
    file_id: str
    filename: str
    file_type: str
    file_size: int
    timestamp: str


class TextExtractionResponse(BaseModel):
    """Response model for text extraction endpoint."""
    file_id: str
    filename: str
    extracted_text: str
    message: str


class AnalysisRequest(BaseModel):
    """Request model for resume analysis."""
    file_id: str = Field(..., description="ID of the uploaded file")
    job_description: str = Field(..., description="Target job description text")


class AnalysisResponse(BaseModel):
    """Response model for resume analysis."""
    file_id: str
    score: float = Field(..., ge=0, le=100, description="Match score 0-100")
    feedback: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
