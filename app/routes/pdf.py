from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.pdf_service import PDFCompressor
from app.utils.file_handler import save_upload_file
import os

router = APIRouter(prefix="/pdf", tags=["PDF Compression"])

@router.post("/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: int = 50
):
    """
    Compress a PDF file
    
    - **file**: PDF file
    - **quality**: Image quality 1-100 (default: 50)
    """
    
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Invalid file type. Only PDFs allowed.")
    
    # Save uploaded file
    input_path = await save_upload_file(file)
    
    # Compress
    result = PDFCompressor.compress(input_path, quality)
    
    if not result["success"]:
        raise HTTPException(500, result["error"])
    
    # Clean up original file
    os.remove(input_path)
    
    return result

@router.get("/download/{filename}")
async def download_compressed_pdf(filename: str):
    """Download compressed PDF"""
    file_path = os.path.join("outputs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )