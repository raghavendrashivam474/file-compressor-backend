import fitz  # PyMuPDF
import os
from app.utils.file_handler import OUTPUT_DIR, get_file_size

class PDFCompressor:
    
    @staticmethod
    def compress(input_path: str, quality: int = 50) -> dict:
        """
        Compress PDF file
        
        Args:
            input_path: Path to original PDF
            quality: Image quality in PDF (1-100)
        
        Returns:
            dict with compression results
        """
        try:
            # Get original size
            original_size = get_file_size(input_path)
            
            # Open PDF
            doc = fitz.open(input_path)
            
            # Generate output filename
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"compressed_{name}.pdf"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            # Compress images in PDF
            for page_num in range(len(doc)):
                page = doc[page_num]
                images = page.get_images()
                
                for img_index, img in enumerate(images):
                    xref = img[0]
                    
                    try:
                        # Extract image
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        
                        # Compress using PIL
                        from PIL import Image
                        import io
                        
                        pil_image = Image.open(io.BytesIO(image_bytes))
                        
                        # Convert to RGB if needed
                        if pil_image.mode in ('RGBA', 'LA', 'P'):
                            pil_image = pil_image.convert('RGB')
                        
                        # Compress
                        compressed_buffer = io.BytesIO()
                        pil_image.save(
                            compressed_buffer,
                            format='JPEG',
                            quality=quality,
                            optimize=True
                        )
                        compressed_bytes = compressed_buffer.getvalue()
                        
                        # Replace image in PDF
                        doc.update_stream(xref, compressed_bytes)
                        
                    except Exception:
                        # Skip if image can't be processed
                        continue
            
            # Save with compression options
            doc.save(
                output_path,
                garbage=4,           # Remove unused objects
                deflate=True,        # Compress streams
                clean=True           # Clean content streams
            )
            doc.close()
            
            # Get compressed size
            compressed_size = get_file_size(output_path)
            
            # Calculate compression ratio
            if original_size > 0:
                compression_ratio = round((1 - compressed_size / original_size) * 100, 2)
            else:
                compression_ratio = 0
            
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