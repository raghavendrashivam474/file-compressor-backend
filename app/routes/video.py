from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.video_service import VideoCompressor
from app.utils.file_handler import save_upload_file
import os

router = APIRouter(prefix="/video", tags=["Video Compression"])

@router.post("/compress")
async def compress_video(
    file: UploadFile = File(...),
    quality: str = "medium",
    resolution: str = None
):
    """
    Compress a video file
    
    - **file**: Video file (mp4, avi, mov, mkv)
    - **quality**: low, medium, high (default: medium)
    - **resolution**: 480p, 720p, 1080p (optional)
    """
    
    # Validate file type
    allowed_types = [
        "video/mp4",
        "video/avi",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-matroska"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Invalid file type. Only videos allowed.")
    
    # Save uploaded file
    input_path = await save_upload_file(file)
    
    # Compress
    result = VideoCompressor.compress(input_path, quality, resolution)
    
    if not result["success"]:
        raise HTTPException(500, result["error"])
    
    # Clean up original file
    os.remove(input_path)
    
    return result

@router.get("/download/{filename}")
async def download_compressed_video(filename: str):
    """Download compressed video"""
    file_path = os.path.join("outputs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename=filename
    )