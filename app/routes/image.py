from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.image_service import ImageCompressor
from app.utils.file_handler import save_upload_file
import os

router = APIRouter(prefix="/image", tags=["Image Compression"])

@router.post("/compress")
async def compress_image(
    file: UploadFile = File(...),
    quality: int = 50
):
    """
    Compress an image file
    
    - **file**: Image file (jpg, png, etc.)
    - **quality**: Compression quality 1-100 (default: 50)
    """
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Invalid file type. Only images allowed.")
    
    # Save uploaded file
    input_path = await save_upload_file(file)
    
    # Compress
    result = ImageCompressor.compress(input_path, quality)
    
    if not result["success"]:
        raise HTTPException(500, result["error"])
    
    # Clean up original file
    os.remove(input_path)
    
    return result

@router.get("/download/{filename}")
async def download_compressed_image(filename: str):
    """Download compressed image"""
    file_path = os.path.join("outputs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    return FileResponse(
        file_path,
        media_type="image/jpeg",
        filename=filename
    )