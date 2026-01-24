"""
Resume Parser Service

This module provides text extraction capabilities for various file formats:
- PDF (with OCR fallback for scanned documents)
- DOCX (Microsoft Word documents)
- TXT (Plain text files)
- Images (JPG, JPEG, PNG) via OCR

Dependencies:
    - pdfplumber: PDF text extraction
    - python-docx: DOCX parsing
    - pytesseract: OCR engine wrapper
    - pdf2image: PDF to image conversion for OCR
    - Pillow: Image processing
"""

import os
import logging
import tempfile
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


def _setup_tesseract() -> bool:
    """
    Setup Tesseract OCR with proper paths and verify language files.
    
    Returns:
        bool: True if Tesseract is properly configured, False otherwise.
    """
    tesseract_path = os.getenv("TESSERACT_PATH")
    
    # Common Tesseract installation paths on Windows
    possible_paths = [
        tesseract_path,
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            tesseract_dir = os.path.dirname(path)
            tessdata_dir = os.path.join(tesseract_dir, "tessdata")
            eng_data = os.path.join(tessdata_dir, "eng.traineddata")
            
            if os.path.exists(tessdata_dir) and os.path.exists(eng_data):
                pytesseract.pytesseract.tesseract_cmd = path
                os.environ["TESSDATA_PREFIX"] = tessdata_dir
                logger.info(f"Tesseract configured: {path}")
                return True
            else:
                logger.warning(f"Tesseract at {path} missing language files")
    
    logger.warning("Tesseract not found. OCR features disabled.")
    return False


# Initialize Tesseract on module load
TESSERACT_AVAILABLE = _setup_tesseract()

# OCR Configuration
PDF_OCR_DPI = int(os.getenv("PDF_OCR_DPI", "300"))
PDF_OCR_LANGUAGE = os.getenv("PDF_OCR_LANGUAGE", "eng")
POPPLER_PATH = os.getenv("POPPLER_PATH")


def _get_tesseract_config() -> str:
    """Build Tesseract configuration string with available languages."""
    tessdata_dir = os.environ.get("TESSDATA_PREFIX", "")
    available_langs = []
    
    for lang in PDF_OCR_LANGUAGE.split("+"):
        lang_file = os.path.join(tessdata_dir, f"{lang}.traineddata")
        if os.path.exists(lang_file):
            available_langs.append(lang)
    
    if not available_langs:
        eng_file = os.path.join(tessdata_dir, "eng.traineddata")
        if os.path.exists(eng_file):
            available_langs = ["eng"]
        else:
            return '--oem 3 --psm 6'
    
    return f'--oem 3 --psm 6 -l {"+".join(available_langs)}'


def is_tesseract_available() -> bool:
    """Check if Tesseract OCR is available."""
    return TESSERACT_AVAILABLE



# PDF EXTRACTION
async def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file.
    
    Uses pdfplumber for text-based PDFs and falls back to OCR
    for scanned/image-based documents.
    
    Args:
        file_path: Path to the PDF file.
        
    Returns:
        Extracted text content.
        
    Raises:
        ValueError: If PDF parsing fails.
    """
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        extracted_text = text.strip()
        
        # Fallback to OCR if insufficient text extracted
        if len(extracted_text) < 50:
            logger.info(f"PDF appears scanned, attempting OCR: {file_path}")
            ocr_text = await _extract_text_from_pdf_ocr(file_path)
            if ocr_text and not ocr_text.startswith("[Warning"):
                return ocr_text
            if not extracted_text:
                return ocr_text
        
        return extracted_text
        
    except Exception as e:
        logger.error(f"PDF parsing error: {e}")
        raise ValueError(f"Failed to parse PDF: {e}")


async def _extract_text_from_pdf_ocr(file_path: str) -> str:
    """
    Extract text from scanned PDF using OCR.
    
    Converts each page to an image and runs Tesseract OCR.
    """
    if not TESSERACT_AVAILABLE:
        return "[Warning: Tesseract OCR not installed. Cannot process scanned PDFs.]"
    
    try:
        from pdf2image import convert_from_path
        from pdf2image.exceptions import PDFPageCountError, PDFInfoNotInstalledError
    except ImportError:
        return "[Warning: pdf2image not installed. Run: pip install pdf2image]"
    
    try:
        convert_kwargs = {"dpi": PDF_OCR_DPI}
        if POPPLER_PATH and os.path.exists(POPPLER_PATH):
            convert_kwargs["poppler_path"] = POPPLER_PATH
        
        images = convert_from_path(file_path, **convert_kwargs)
        
    except PDFInfoNotInstalledError:
        return "[Warning: Poppler not installed. Required for PDF OCR.]"
    except PDFPageCountError:
        return "[Warning: Could not read PDF pages. File may be corrupted.]"
    except Exception as e:
        return f"[Warning: PDF conversion failed: {e}]"
    
    # OCR each page
    all_text = []
    config = _get_tesseract_config()
    
    for i, image in enumerate(images):
        try:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            page_text = pytesseract.image_to_string(image, config=config)
            if page_text.strip():
                all_text.append(f"--- Page {i + 1} ---\n{page_text.strip()}")
        except Exception as e:
            logger.warning(f"OCR failed for page {i + 1}: {e}")
            continue
    
    if all_text:
        return "\n\n".join(all_text)
    return "[Warning: OCR completed but no text could be extracted.]"



# DOCX EXTRACTION
async def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file.
    
    Args:
        file_path: Path to the DOCX file.
        
    Returns:
        Extracted text content.
        
    Raises:
        ValueError: If DOCX parsing fails.
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text.strip()
    except Exception as e:
        logger.error(f"DOCX parsing error: {e}")
        raise ValueError(f"Failed to parse DOCX: {e}")



# TXT EXTRACTION
async def extract_text_from_txt(file_path: str) -> str:
    """
    Read text from TXT file with encoding fallback.
    
    Args:
        file_path: Path to the TXT file.
        
    Returns:
        File text content.
        
    Raises:
        ValueError: If file reading fails.
    """
    encodings = ['utf-8', 'latin-1', 'cp1256']  # Added Arabic encoding
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read().strip()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logger.error(f"TXT reading error: {e}")
            raise ValueError(f"Failed to read TXT: {e}")
    
    raise ValueError("Failed to decode TXT file with any encoding")



# IMAGE EXTRACTION (OCR)
async def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from image using OCR.
    
    Args:
        file_path: Path to the image file (JPG, JPEG, PNG).
        
    Returns:
        Extracted text content.
        
    Raises:
        ValueError: If OCR processing fails.
    """
    if not TESSERACT_AVAILABLE:
        return "[Warning: Tesseract OCR not installed. Cannot process images.]"
    
    temp_file = None
    try:
        image = Image.open(file_path)
        image = image.convert("RGB")
        
        # Save as TIFF for better Tesseract compatibility
        with tempfile.NamedTemporaryFile(suffix=".tiff", delete=False) as tmp:
            temp_file = tmp.name
            image.save(temp_file, format="TIFF")
        
        config = _get_tesseract_config()
        text = pytesseract.image_to_string(temp_file, config=config)
        
        if not text.strip():
            return "[Warning: No text could be extracted from this image.]"
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Image OCR error: {e}")
        raise ValueError(f"Failed to process image: {e}")
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass


# MAIN PARSER FUNCTION
async def parse_resume(file_path: str, file_ext: str) -> str:
    """
    Parse resume file and extract text content.
    
    Delegates to appropriate parser based on file extension.
    
    Args:
        file_path: Path to the resume file.
        file_ext: File extension (e.g., '.pdf', '.docx').
        
    Returns:
        Extracted text content.
        
    Raises:
        ValueError: If file format is unsupported or parsing fails.
        
    Supported formats:
        - PDF: Text extraction with OCR fallback
        - DOCX: Microsoft Word documents
        - TXT: Plain text files
        - JPG/JPEG/PNG: OCR text extraction
    """
    file_ext = file_ext.lower()
    logger.info(f"Parsing: {file_path} ({file_ext})")
    
    parsers = {
        '.pdf': extract_text_from_pdf,
        '.docx': extract_text_from_docx,
        '.txt': extract_text_from_txt,
        '.jpg': extract_text_from_image,
        '.jpeg': extract_text_from_image,
        '.png': extract_text_from_image,
    }
    
    parser = parsers.get(file_ext)
    if not parser:
        raise ValueError(f"Unsupported file format: {file_ext}")
    
    return await parser(file_path)
