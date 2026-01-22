FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PDF parsing and OCR
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
