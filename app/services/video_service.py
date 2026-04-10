import subprocess
import os
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
            
            # Build FFmpeg command
            cmd = ['ffmpeg', '-i', input_path, '-y']
            
            # Apply resolution if specified
            if resolution:
                height_map = {
                    "480p": "480",
                    "720p": "720",
                    "1080p": "1080"
                }
                height = height_map.get(resolution)
                if height:
                    cmd.extend(['-vf', f'scale=-2:{height}'])
            
            # Add compression settings
            cmd.extend([
                '-vcodec', 'libx264',
                '-crf', str(crf),
                '-preset', 'medium',
                '-acodec', 'aac',
                '-b:a', '128k',
                output_path
            ])
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"FFmpeg error: {result.stderr}"
                }
            
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
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Video compression timed out. Try a smaller file."
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "FFmpeg not installed on server. Video compression unavailable."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }