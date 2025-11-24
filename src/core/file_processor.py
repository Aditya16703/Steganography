"""
File processing utilities for SteganoGuard Pro
"""

import os
import hashlib
from typing import List, Dict, Optional
from pathlib import Path

class FileProcessor:
    """
    Handles file operations for steganography
    """
    
    def __init__(self):
        self.supported_extensions = {
            'images': ['.png', '.jpg', '.jpeg', '.bmp', '.tiff'],
            'documents': ['.txt', '.pdf', '.doc', '.docx'],
            'archives': ['.zip', '.rar'],
            'audio': ['.wav', '.mp3']
        }
    
    def analyze_file(self, file_path: str) -> Dict:
        """
        Comprehensive file analysis
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        path = Path(file_path)
        stat = path.stat()
        
        analysis = {
            'basic_info': {
                'filename': path.name,
                'extension': path.suffix.lower(),
                'size_bytes': stat.st_size,
                'size_formatted': self._format_size(stat.st_size),
                'path': file_path
            },
            'security_info': {
                'hash_md5': self._calculate_file_hash(file_path, 'md5'),
                'hash_sha256': self._calculate_file_hash(file_path, 'sha256'),
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK)
            }
        }
        
        return analysis
    
    def validate_file_for_steganography(self, file_path: str) -> tuple:
        """
        Validate if file is suitable for steganography
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file size (max 100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        file_size = os.path.getsize(file_path)
        
        if file_size > max_size:
            return False, f"File too large ({self._format_size(file_size)})"
        
        # Check extension
        ext = Path(file_path).suffix.lower()
        if ext not in self.supported_extensions['images']:
            return False, f"Unsupported file format: {ext}"
        
        return True, "File is valid"
    
    def create_backup(self, original_path: str) -> str:
        """
        Create backup of file
        """
        backup_path = original_path + '.backup'
        import shutil
        shutil.copy2(original_path, backup_path)
        return backup_path
    
    def batch_process_files(self, directory: str, operation: str) -> List[Dict]:
        """
        Process multiple files in a directory
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        results = []
        for file_path in self._find_supported_files(directory):
            try:
                analysis = self.analyze_file(file_path)
                analysis['operation'] = operation
                analysis['status'] = 'success'
                results.append(analysis)
            except Exception as e:
                results.append({
                    'file': file_path,
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    def _calculate_file_hash(self, file_path: str, algorithm: str) -> str:
        """Calculate file hash"""
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def _find_supported_files(self, directory: str) -> List[str]:
        """Find supported files in directory"""
        supported_files = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                ext = Path(file_path).suffix.lower()
                if ext in self.supported_extensions['images']:
                    supported_files.append(file_path)
        
        return supported_files