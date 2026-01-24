import os
import logging
from pathlib import Path
from typing import Optional
import pdfplumber
import docx
import pytesseract
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Configure Tesseract Path if provided in env
tesseract_path = os.getenv("TESSERACT_PATH")
if tesseract_path and os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

async def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using pdfplumber"""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing PDF {file_path}: {str(e)}")
        raise ValueError(f"Failed to parse PDF: {str(e)}")

async def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing DOCX {file_path}: {str(e)}")
        raise ValueError(f"Failed to parse DOCX: {str(e)}")

async def extract_text_from_txt(file_path: str) -> str:
    """Read text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except UnicodeDecodeError:
        # Try different encoding if utf-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error reading TXT {file_path}: {str(e)}")
            raise ValueError(f"Failed to read TXT: {str(e)}")
    except Exception as e:
        logger.error(f"Error reading TXT {file_path}: {str(e)}")
        raise ValueError(f"Failed to read TXT: {str(e)}")

async def extract_text_from_image(file_path: str) -> str:
    """Extract text from image using OCR (Tesseract)"""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing Image {file_path}: {str(e)}")
        raise ValueError(f"Failed to parse Image (OCR error): {str(e)}")

async def parse_resume(file_path: str, file_ext: str) -> str:
    """
    Main parser function that delegates to specific parsers based on file extension
    """
    file_ext = file_ext.lower()
    
    if file_ext == '.pdf':
        return await extract_text_from_pdf(file_path)
    elif file_ext in ['.docx']:
        return await extract_text_from_docx(file_path)
    elif file_ext == '.txt':
        return await extract_text_from_txt(file_path)
    elif file_ext in ['.jpg', '.jpeg', '.png']:
        return await extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")
