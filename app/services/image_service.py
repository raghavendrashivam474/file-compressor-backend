from PIL import Image
import os
from app.utils.file_handler import OUTPUT_DIR, get_file_size

class ImageCompressor:
    
    @staticmethod
    def compress(input_path: str, quality: int = 50) -> dict:
        """
        Compress image and return result info
        
        Args:
            input_path: Path to original image
            quality: Compression quality (1-100)
        
        Returns:
            dict with output_path, original_size, compressed_size, compression_ratio
        """
        try:
            # Get original size
            original_size = get_file_size(input_path)
            
            # Open image
            img = Image.open(input_path)
            
            # Convert RGBA to RGB if needed (for JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Generate output filename
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"compressed_{name}.jpg"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            # Compress and save
            img.save(
                output_path,
                "JPEG",
                quality=quality,
                optimize=True,
                progressive=True
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
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }