"""
Resume Parser Service

Provides text extraction from various document formats with OCR support.
"""

from .parser import parse_resume, is_tesseract_available

__all__ = ['parse_resume', 'is_tesseract_available']
