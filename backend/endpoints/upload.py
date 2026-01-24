"""
File Upload API Endpoints

Handles resume file upload, storage, and text extraction.
"""

import os
import uuid
import logging
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException

from models import FileUploadResponse, TextExtractionResponse
from services.parser import parse_resume

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["upload"])

# Configuration
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def _validate_file(filename: str, file_size: int) -> tuple[bool, str]:
    """
    Validate uploaded file extension and size.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB"
    
    return True, ""


@router.post("/upload", response_model=FileUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume file for analysis.
    
    Accepts: PDF, DOCX, DOC, PNG, JPG, JPEG, TXT
    Max size: 10MB
    
    Returns:
        FileUploadResponse with file_id for subsequent operations.
    """
    try:
        content = await file.read()
        file_size = len(content)
        
        is_valid, error_msg = _validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Generate unique file ID and save
        file_id = str(uuid.uuid4())
        file_ext = Path(file.filename).suffix
        saved_filename = f"{file_id}{file_ext}"
        file_path = UPLOAD_DIR / saved_filename
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"File uploaded: {file.filename} -> {saved_filename}")
        
        return FileUploadResponse(
            success=True,
            message="File uploaded successfully",
            file_id=file_id,
            filename=file.filename,
            file_type=file_ext[1:],
            file_size=file_size,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload file")


@router.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """Get information about an uploaded file."""
    for file_path in UPLOAD_DIR.glob(f"{file_id}.*"):
        return {
            "file_id": file_id,
            "exists": True,
            "filename": file_path.name,
            "size": file_path.stat().st_size
        }
    
    raise HTTPException(status_code=404, detail="File not found")


@router.get("/extract/{file_id}", response_model=TextExtractionResponse)
async def extract_text(file_id: str):
    """
    Extract and return text content from an uploaded resume.
    
    Supports PDF (with OCR for scanned docs), DOCX, TXT, and images.
    """
    file_path = None
    file_ext = None
    
    for path in UPLOAD_DIR.glob(f"{file_id}.*"):
        file_path = path
        file_ext = path.suffix
        break
    
    if not file_path:
        raise HTTPException(status_code=404, detail="Resume file not found")
    
    try:
        text = await parse_resume(str(file_path), file_ext)
        
        return TextExtractionResponse(
            file_id=file_id,
            filename=file_path.name,
            extracted_text=text,
            message="Text extracted successfully"
        )
    except Exception as e:
        logger.error(f"Extraction error for {file_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text: {e}"
        )
