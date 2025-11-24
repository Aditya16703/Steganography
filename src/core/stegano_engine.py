import numpy as np
from PIL import Image, ImageOps
import zlib
import hashlib
import struct
from typing import Tuple, Optional, Dict
import os

class SteganoEngine:
    """
    Advanced steganography engine with multiple techniques
    and enhanced security features
    """
    
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        self.techniques = ['LSB', 'LSB_RANDOM', 'MULTI_CHANNEL']
        
    def embed_data_secure(self, image_path: str, data: bytes, 
                         password: str = "", bits: int = 2, 
                         technique: str = 'LSB') -> Tuple[np.ndarray, Dict]:
        """
        Embed data with enhanced security features
        
        Args:
            image_path: Path to cover image
            data: Data to hide
            password: Encryption password
            bits: LSB bits to use (1-4)
            technique: Embedding technique
            
        Returns:
            Tuple of (stego_image, metadata)
        """
        # Validate inputs
        self._validate_inputs(image_path, data, bits)
        
        # Load and prepare image
        image = Image.open(image_path)
        if image.mode not in ['RGB', 'RGBA']:
            image = image.convert('RGB')
        
        img_array = np.array(image)
        
        # Prepare data with security features
        processed_data = self._prepare_data_with_security(data, password)
        
        # Embed using selected technique
        if technique == 'LSB':
            stego_array = self._lsb_embed_secure(img_array, processed_data, bits)
        elif technique == 'LSB_RANDOM':
            stego_array = self._lsb_random_embed(img_array, processed_data, bits, password)
        else:
            stego_array = self._lsb_embed_secure(img_array, processed_data, bits)
        
        # Generate comprehensive metadata
        metadata = self._generate_metadata(
            image_path, data, processed_data, bits, technique, password
        )
        
        return stego_array, metadata
    
    def extract_data_secure(self, image_path: str, password: str = "", 
                           bits: int = 2, technique: str = 'LSB') -> Tuple[bytes, Dict]:
        """
        Extract hidden data with validation
        
        Args:
            image_path: Path to stego image
            password: Decryption password
            bits: LSB bits used
            technique: Extraction technique
            
        Returns:
            Tuple of (extracted_data, metadata)
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image
        image = Image.open(image_path)
        img_array = np.array(image)
        
        # Extract data based on technique
        if technique == 'LSB_RANDOM':
            extracted_bytes = self._lsb_random_extract(img_array, bits, password)
        else:
            extracted_bytes = self._lsb_extract_secure(img_array, bits)
        
        # Process and validate extracted data
        original_data, extraction_info = self._process_extracted_data(
            extracted_bytes, password
        )
        
        return original_data, extraction_info
    
    def analyze_capacity(self, image_path: str) -> Dict:
        """
        Comprehensive capacity analysis
        
        Args:
            image_path: Path to image
            
        Returns:
            Capacity analysis dictionary
        """
        image = Image.open(image_path)
        img_array = np.array(image)
        
        analysis = {
            'image_info': {
                'dimensions': img_array.shape,
                'total_pixels': img_array.size,
                'channels': img_array.shape[2] if len(img_array.shape) > 2 else 1,
                'mode': image.mode
            },
            'capacity_analysis': {},
            'security_recommendations': []
        }
        
        # Calculate capacity for different configurations
        for bit_depth in [1, 2, 3, 4]:
            capacity_bits = img_array.size * bit_depth
            capacity_bytes = (capacity_bits - 256) // 8  # Reserve for header
            
            analysis['capacity_analysis'][f'{bit_depth}_bit_lsb'] = {
                'bytes': capacity_bytes,
                'kilobytes': round(capacity_bytes / 1024, 2),
                'megabytes': round(capacity_bytes / (1024 * 1024), 3),
                'bits_used': bit_depth
            }
        
        # Security recommendations
        if img_array.shape[0] * img_array.shape[1] > 1000000:  # Large image
            analysis['security_recommendations'].append(
                "Use 1-2 bit LSB for better stealth in large images"
            )
        else:
            analysis['security_recommendations'].append(
                "Use 2-4 bit LSB for optimal capacity in small images"
            )
        
        return analysis
    
    def _validate_inputs(self, image_path: str, data: bytes, bits: int):
        """Validate all input parameters"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        if bits not in [1, 2, 3, 4]:
            raise ValueError("Bits must be between 1 and 4")
        
        if len(data) == 0:
            raise ValueError("Data cannot be empty")
    
    def _prepare_data_with_security(self, data: bytes, password: str) -> bytes:
        """Prepare data with compression and optional encryption"""
        from .crypto_manager import CryptoManager
        
        # Compress data
        compressed_data = zlib.compress(data, level=9)
        
        # Encrypt if password provided
        if password:
            crypto = CryptoManager()
            compressed_data = crypto.encrypt(compressed_data, password)
        
        # Create secure header
        header = self._create_secure_header(data, compressed_data, bool(password))
        
        return header + compressed_data
    
    def _create_secure_header(self, original_data: bytes, 
                            processed_data: bytes, encrypted: bool) -> bytes:
        """Create secure header with metadata"""
        import time
        
        header_data = {
            'magic': b'STEGANO01',
            'timestamp': int(time.time()),
            'original_size': len(original_data),
            'processed_size': len(processed_data),
            'encrypted': 1 if encrypted else 0,
            'compressed': 1,
            'checksum': hashlib.sha256(original_data).digest()[:16]
        }
        
        # Pack header
        header = header_data['magic']
        header += struct.pack('>Q', header_data['timestamp'])
        header += struct.pack('>I', header_data['original_size'])
        header += struct.pack('>I', header_data['processed_size'])
        header += struct.pack('>B', header_data['encrypted'])
        header += struct.pack('>B', header_data['compressed'])
        header += header_data['checksum']
        
        return header
    
    def _lsb_embed_secure(self, img_array: np.ndarray, data: bytes, bits: int) -> np.ndarray:
        """Secure LSB embedding with validation"""
        # Convert data to binary with end marker
        binary_data = ''.join(format(byte, '08b') for byte in data)
        binary_data += '1111111111111110'  # 16-bit end marker
        
        flat_img = img_array.flatten()
        
        # Validate capacity
        required_bits = len(binary_data)
        available_bits = len(flat_img) * bits
        
        if required_bits > available_bits:
            raise ValueError(
                f"Insufficient capacity: {required_bits} bits needed, "
                f"{available_bits} bits available"
            )
        
        # Embed data
        data_index = 0
        for i in range(len(flat_img)):
            if data_index >= required_bits:
                break
            
            current_val = flat_img[i]
            mask = (255 >> bits) << bits
            cleared_val = current_val & mask
            
            chunk = binary_data[data_index:data_index + bits]
            if chunk:
                new_lsb = int(chunk.ljust(bits, '0'), 2)
                new_val = cleared_val | new_lsb
                flat_img[i] = new_val
            
            data_index += bits
        
        return flat_img.reshape(img_array.shape)
    
    def _lsb_random_embed(self, img_array: np.ndarray, data: bytes, 
                         bits: int, password: str) -> np.ndarray:
        """Randomized LSB embedding for enhanced security"""
        import hashlib
        
        # Use password to seed random generator
        seed = hashlib.sha256(password.encode()).digest()
        rng = np.random.RandomState(int.from_bytes(seed[:4], 'big'))
        
        flat_img = img_array.flatten()
        indices = rng.permutation(len(flat_img))
        
        binary_data = ''.join(format(byte, '08b') for byte in data)
        binary_data += '1111111111111110'
        
        data_index = 0
        for idx in indices:
            if data_index >= len(binary_data):
                break
            
            current_val = flat_img[idx]
            mask = (255 >> bits) << bits
            cleared_val = current_val & mask
            
            chunk = binary_data[data_index:data_index + bits]
            if chunk:
                new_lsb = int(chunk.ljust(bits, '0'), 2)
                new_val = cleared_val | new_lsb
                flat_img[idx] = new_val
            
            data_index += bits
        
        return flat_img.reshape(img_array.shape)
    
    def _lsb_extract_secure(self, img_array: np.ndarray, bits: int) -> bytes:
        """Secure LSB extraction with validation"""
        flat_img = img_array.flatten()
        
        binary_data = ""
        for pixel in flat_img:
            lsb_bits = pixel & ((1 << bits) - 1)
            binary_data += format(lsb_bits, f'0{bits}b')
        
        # Find end marker
        end_marker = '1111111111111110'
        if end_marker in binary_data:
            binary_data = binary_data[:binary_data.index(end_marker)]
        
        # Convert to bytes
        bytes_data = bytearray()
        for i in range(0, len(binary_data), 8):
            byte_str = binary_data[i:i+8]
            if len(byte_str) == 8:
                bytes_data.append(int(byte_str, 2))
        
        return bytes(bytes_data)
    
    def _lsb_random_extract(self, img_array: np.ndarray, bits: int, 
                           password: str) -> bytes:
        """Extract from randomized embedding"""
        import hashlib
        
        seed = hashlib.sha256(password.encode()).digest()
        rng = np.random.RandomState(int.from_bytes(seed[:4], 'big'))
        
        flat_img = img_array.flatten()
        indices = rng.permutation(len(flat_img))
        
        binary_data = ['' for _ in range(len(flat_img))]
        
        for pos, idx in enumerate(indices):
            pixel = flat_img[idx]
            lsb_bits = pixel & ((1 << bits) - 1)
            binary_data[idx] = format(lsb_bits, f'0{bits}b')
        
        full_binary = ''.join(binary_data)
        
        # Find end marker
        end_marker = '1111111111111110'
        if end_marker in full_binary:
            full_binary = full_binary[:full_binary.index(end_marker)]
        
        # Convert to bytes
        bytes_data = bytearray()
        for i in range(0, len(full_binary), 8):
            byte_str = full_binary[i:i+8]
            if len(byte_str) == 8:
                bytes_data.append(int(byte_str, 2))
        
        return bytes(bytes_data)
    
    def _process_extracted_data(self, extracted_bytes: bytes, 
                               password: str) -> Tuple[bytes, Dict]:
        """Process and validate extracted data"""
        try:
            # Parse header
            if len(extracted_bytes) < 32:  # Minimum header size
                return extracted_bytes, {'legacy_mode': True}
            
            magic = extracted_bytes[:9]
            if magic != b'STEGANO01':
                return extracted_bytes, {'legacy_mode': True}
            
            # Extract header fields
            timestamp = struct.unpack('>Q', extracted_bytes[9:17])[0]
            original_size = struct.unpack('>I', extracted_bytes[17:21])[0]
            processed_size = struct.unpack('>I', extracted_bytes[21:25])[0]
            encrypted = struct.unpack('>B', extracted_bytes[25:26])[0]
            compressed = struct.unpack('>B', extracted_bytes[26:27])[0]
            checksum = extracted_bytes[27:43]
            
            data_part = extracted_bytes[43:43 + processed_size]
            
            # Decrypt if necessary
            if encrypted and password:
                from .crypto_manager import CryptoManager
                crypto = CryptoManager()
                data_part = crypto.decrypt(data_part, password)
            
            # Decompress if necessary
            if compressed:
                data_part = zlib.decompress(data_part)
            
            # Verify checksum
            calculated_checksum = hashlib.sha256(data_part).digest()[:16]
            integrity_ok = checksum == calculated_checksum
            
            extraction_info = {
                'success': True,
                'timestamp': timestamp,
                'original_size': original_size,
                'encrypted': bool(encrypted),
                'compressed': bool(compressed),
                'integrity_verified': integrity_ok,
                'extraction_method': 'secure'
            }
            
            return data_part, extraction_info
            
        except Exception as e:
            # Fallback to legacy processing
            try:
                decompressed = zlib.decompress(extracted_bytes)
                return decompressed, {'legacy_mode': True, 'success': True}
            except:
                return extracted_bytes, {'success': False, 'error': str(e)}
    
    def _generate_metadata(self, image_path: str, original_data: bytes,
                          processed_data: bytes, bits: int, 
                          technique: str, password: str) -> Dict:
        """Generate comprehensive embedding metadata"""
        import os
        from datetime import datetime
        
        file_stats = os.stat(image_path)
        
        return {
            'embedding_info': {
                'technique': technique,
                'bits_used': bits,
                'timestamp': datetime.now().isoformat(),
                'password_used': bool(password)
            },
            'data_info': {
                'original_size': len(original_data),
                'processed_size': len(processed_data),
                'compression_ratio': f"{(len(processed_data)/len(original_data))*100:.1f}%",
                'security_level': 'High' if password else 'Medium'
            },
            'image_info': {
                'filename': os.path.basename(image_path),
                'file_size': file_stats.st_size,
                'last_modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
            }
        }