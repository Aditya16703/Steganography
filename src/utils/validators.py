"""
Validation utilities for SteganoGuard Pro
"""

import os
from pathlib import Path
from typing import Tuple

class Validators:
    """
    Input validation utilities
    """
    
    @staticmethod
    def validate_image_path(image_path: str) -> Tuple[bool, str]:
        """
        Validate image file path
        """
        if not image_path or not image_path.strip():
            return False, "No image path provided"
        
        if not os.path.exists(image_path):
            return False, "Image file does not exist"
        
        # Check if it's a file (not directory)
        if not os.path.isfile(image_path):
            return False, "Path is not a file"
        
        # Check file extension
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']
        ext = Path(image_path).suffix.lower()
        if ext not in valid_extensions:
            return False, f"Unsupported image format: {ext}"
        
        # Check file size (max 50MB)
        max_size = 50 * 1024 * 1024
        file_size = os.path.getsize(image_path)
        if file_size > max_size:
            return False, f"Image file too large ({file_size / (1024*1024):.1f}MB)"
        
        return True, "Image path is valid"
    
    @staticmethod
    def validate_password(password: str, confirm_password: str = None) -> Tuple[bool, str]:
        """
        Validate password strength
        """
        if not password:
            return True, ""  # Empty password is allowed (no encryption)
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        
        if len(password) > 100:
            return False, "Password too long"
        
        if confirm_password is not None and password != confirm_password:
            return False, "Passwords do not match"
        
        return True, "Password is valid"
    
    @staticmethod
    def validate_lsb_bits(bits: int) -> Tuple[bool, str]:
        """
        Validate LSB bits parameter
        """
        if not isinstance(bits, int):
            return False, "Bits must be an integer"
        
        if bits < 1 or bits > 4:
            return False, "Bits must be between 1 and 4"
        
        return True, "Bits value is valid"
    
    @staticmethod
    def validate_output_path(output_path: str, overwrite: bool = False) -> Tuple[bool, str]:
        """
        Validate output file path
        """
        if not output_path or not output_path.strip():
            return False, "No output path provided"
        
        # Check if file already exists
        if os.path.exists(output_path) and not overwrite:
            return False, "Output file already exists"
        
        # Check directory permissions
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                return False, f"Cannot create directory: {str(e)}"
        
        # Check file extension
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        ext = Path(output_path).suffix.lower()
        if ext not in valid_extensions:
            return False, f"Unsupported output format: {ext}"
        
        return True, "Output path is valid"
    
    @staticmethod
    def validate_text_data(text: str) -> Tuple[bool, str]:
        """
        Validate text data for hiding
        """
        if not text or not text.strip():
            return False, "Text cannot be empty"
        
        if len(text.encode('utf-8')) > 10 * 1024 * 1024:  # 10MB max
            return False, "Text too large"
        
        return True, "Text is valid"