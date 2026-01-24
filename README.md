# Resume AI Platform 🚀

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-powered resume analysis platform with intelligent text extraction, OCR support, and explainable feedback.

## ✨ Features

- 📄 **Multi-format Support**: PDF, DOCX, TXT, and images (JPG, PNG)
- 🔍 **Smart OCR**: Automatic text extraction from scanned documents
- 🧠 **PDF Intelligence**: Detects scanned PDFs and applies OCR automatically
- ⚡ **RESTful API**: FastAPI backend with OpenAPI documentation

## 🏗️ Project Structure

```
resume-ai-platform/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Dependencies
│   ├── endpoints/
│   │   └── upload.py        # Upload & extraction API
│   └── services/
│       └── parser.py        # Resume parser (OCR + text)
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) (Windows)

### Installation

```bash
# Clone
git clone https://github.com/Latreche-khalil14/resume-ai-platform.git
cd resume-ai-platform/backend

# Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure
cp .env.example .env

# Run
python main.py
```

**API Docs**: http://localhost:8000/docs

## 📡 API Endpoints

| Method | Endpoint                 | Description   |
| ------ | ------------------------ | ------------- |
| `GET`  | `/`                      | API info      |
| `GET`  | `/health`                | Health check  |
| `POST` | `/api/upload`            | Upload resume |
| `GET`  | `/api/extract/{file_id}` | Extract text  |

## ⚙️ Configuration

```env
# .env
TESSERACT_PATH=C:\Program Files (x86)\Tesseract-OCR\tesseract.exe
POPPLER_PATH=C:\poppler\Library\bin
PDF_OCR_DPI=300
PDF_OCR_LANGUAGE=eng
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.12
- **OCR**: Tesseract, pytesseract, pdf2image
- **Parsing**: pdfplumber, python-docx, Pillow

## 📝 License

MIT License

## 👤 Author

**Latreche Khalil**

- GitHub: [@Latreche-khalil14](https://github.com/Latreche-khalil14)

---

Built with ❤️ using FastAPI and AI
