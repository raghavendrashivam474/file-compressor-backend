# 🗜️ File Compressor API

A powerful FastAPI backend for compressing images, PDFs, and videos with industry-leading compression ratios.

## ✨ Features

- **Image Compression** (80-95% reduction) using Pillow
- **PDF Compression** (40-50% reduction) using PyMuPDF
- **Video Compression** (up to 97% reduction) using FFmpeg
- RESTful API design
- Auto-generated Swagger documentation
- CORS enabled for web clients

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg (for video compression)

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd compressor-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Run Server
Bash

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
Visit: http://localhost:8001/docs for API documentation

📊 Results Achieved
Images: 80-95% compression
PDFs: 40-50% compression
Videos: 35-97% compression
🛠️ Tech Stack
FastAPI
Uvicorn
Pillow (PIL)
PyMuPDF
FFmpeg-python
📡 API Endpoints
Image Compression
POST /api/v1/image/compress - Compress image
GET /api/v1/image/download/{filename} - Download compressed image
PDF Compression
POST /api/v1/pdf/compress - Compress PDF
GET /api/v1/pdf/download/{filename} - Download compressed PDF
Video Compression
POST /api/v1/video/compress - Compress video
GET /api/v1/video/download/{filename} - Download compressed video
📄 License
MIT License