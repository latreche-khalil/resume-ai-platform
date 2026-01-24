import asyncio
import os
import sys

# Add backend directory to path to import services correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.parser import parse_resume, is_tesseract_available
from docx import Document

async def test_parser():
    print("🚀 Starting Parser Test...\n")
    print("=" * 50)

    # Check Tesseract availability
    print("\n📋 System Check:")
    if is_tesseract_available():
        print("✅ Tesseract OCR is available")
    else:
        print("⚠️  Tesseract OCR is NOT available - OCR features will not work")
        print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Check Poppler availability
    try:
        from pdf2image import convert_from_path
        print("✅ pdf2image library is available")
    except ImportError:
        print("⚠️  pdf2image is NOT installed - PDF OCR will not work")
        print("   Install with: pip install pdf2image")

    print("\n" + "=" * 50)

    # 1. Test TXT
    txt_path = "test_resume.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("This is a test resume content from a TXT file.\nName: John Doe\nSkills: Python, FastAPI")
    
    print(f"\n📄 Testing TXT ({txt_path})...")
    try:
        text = await parse_resume(txt_path, ".txt")
        print(f"✅ TXT Parsed Successfully!")
        print(f"   Content preview: '{text[:100]}...'")
    except Exception as e:
        print(f"❌ TXT Failed: {e}")

    # 2. Test DOCX
    docx_path = "test_resume.docx"
    doc = Document()
    doc.add_paragraph("This is a test resume content from a DOCX file.")
    doc.add_paragraph("Name: Jane Smith")
    doc.add_paragraph("Skills: Java, Spring Boot, Docker")
    doc.save(docx_path)

    print(f"\n📄 Testing DOCX ({docx_path})...")
    try:
        text = await parse_resume(docx_path, ".docx")
        print(f"✅ DOCX Parsed Successfully!")
        print(f"   Content preview: '{text[:100]}...'")
    except Exception as e:
        print(f"❌ DOCX Failed: {e}")

    # 3. Test PDF (if any exists in uploads)
    print(f"\n📄 Testing PDF from uploads folder...")
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    if os.path.exists(uploads_dir):
        pdf_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
        if pdf_files:
            pdf_path = os.path.join(uploads_dir, pdf_files[0])
            print(f"   Found PDF: {pdf_files[0]}")
            try:
                text = await parse_resume(pdf_path, ".pdf")
                if text.startswith("[Warning"):
                    print(f"⚠️  PDF parsed with warning: {text[:200]}")
                else:
                    print(f"✅ PDF Parsed Successfully!")
                    print(f"   Content preview: '{text[:150]}...'")
            except Exception as e:
                print(f"❌ PDF Failed: {e}")
        else:
            print("   No PDF files found in uploads folder")
    else:
        print("   Uploads folder not found")

    # Cleanup
    try:
        os.remove(txt_path)
        os.remove(docx_path)
        print("\n🧹 Cleanup done.")
    except:
        pass

    print("\n" + "=" * 50)
    print("✨ Parser test completed!")

if __name__ == "__main__":
    asyncio.run(test_parser())
