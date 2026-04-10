import os

# Set FFmpeg paths directly (no PATH needed!)
os.environ['FFMPEG_BINARY'] = r'C:\ffmpeg\bin\ffmpeg.exe'
os.environ['FFPROBE_BINARY'] = r'C:\ffmpeg\bin\ffprobe.exe'

import ffmpeg
from app.utils.file_handler import OUTPUT_DIR, get_file_size

class VideoCompressor:
    
    @staticmethod
    def compress(
        input_path: str,
        quality: str = "medium",
        resolution: str = None
    ) -> dict:
        """
        Compress video file
        
        Args:
            input_path: Path to original video
            quality: low, medium, high
            resolution: 480p, 720p, 1080p (optional)
        
        Returns:
            dict with compression results
        """
        try:
            # Get original size
            original_size = get_file_size(input_path)
            
            # Quality presets (CRF values)
            crf_map = {
                "low": 28,      # Smaller file, lower quality
                "medium": 23,   # Balanced
                "high": 18      # Better quality, larger file
            }
            crf = crf_map.get(quality, 23)
            
            # Generate output filename
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"compressed_{name}.mp4"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            # Build FFmpeg stream
            stream = ffmpeg.input(input_path)
            
            # Apply resolution if specified
            if resolution:
                height_map = {
                    "480p": 480,
                    "720p": 720,
                    "1080p": 1080
                }
                height = height_map.get(resolution)
                if height:
                    stream = ffmpeg.filter(stream, 'scale', -2, height)
            
            # Output with H.264 codec
            stream = ffmpeg.output(
                stream,
                output_path,
                vcodec='libx264',
                crf=crf,
                preset='medium',
                acodec='aac',
                audio_bitrate='128k'
            )
            
            # Run FFmpeg with explicit binary path
            ffmpeg.run(
                stream,
                cmd=r'C:\ffmpeg\bin\ffmpeg.exe',
                overwrite_output=True,
                capture_stdout=True,
                capture_stderr=True
            )
            
            # Get compressed size
            compressed_size = get_file_size(output_path)
            
            # Calculate compression ratio
            compression_ratio = round((1 - compressed_size / original_size) * 100, 2)
            
            return {
                "success": True,
                "output_path": output_path,
                "output_filename": output_filename,
                "original_size_mb": original_size,
                "compressed_size_mb": compressed_size,
                "compression_ratio": f"{compression_ratio}%",
                "message": f"Compressed from {original_size}MB to {compressed_size}MB"
            }
            
        except ffmpeg.Error as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            return {
                "success": False,
                "error": f"FFmpeg error: {error_message}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }