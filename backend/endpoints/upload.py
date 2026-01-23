from fastapi import APIRouter, UploadFile, File, HTTPException
from models import FileUploadResponse
import uuid
import os
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["upload"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def validate_file(filename: str, file_size: int) -> tuple[bool, str]:
    """
    Validate uploaded file
    
    Args:
        filename: Name of the uploaded file
        file_size: Size of the file in bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check size
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB"
    
    return True, ""


@router.post("/upload", response_model=FileUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload resume file for analysis
    
    Accepts: PDF, DOCX, DOC, PNG, JPG, JPEG
    Max size: 10MB
    """
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file
        is_valid, error_msg = validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        file_ext = Path(file.filename).suffix
        saved_filename = f"{file_id}{file_ext}"
        file_path = UPLOAD_DIR / saved_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"File uploaded: {file.filename} -> {saved_filename}")
        
        return FileUploadResponse(
            success=True,
            message="File uploaded successfully",
            file_id=file_id,
            filename=file.filename,
            file_type=file_ext[1:],  # Remove dot
            file_size=file_size,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to upload file"
        )


@router.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """Get information about an uploaded file"""
    # Find file
    for file_path in UPLOAD_DIR.glob(f"{file_id}.*"):
        return {
            "file_id": file_id,
            "exists": True,
            "filename": file_path.name,
            "size": file_path.stat().st_size
        }
    
    raise HTTPException(status_code=404, detail="File not found")
