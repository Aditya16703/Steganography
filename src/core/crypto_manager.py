import hashlib
import base64

# Handle both Cryptodome and Crypto imports
try:
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad, unpad
    from Cryptodome.Random import get_random_bytes
    CRYPTO_AVAILABLE = True
except ImportError:
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
        from Crypto.Random import get_random_bytes
        CRYPTO_AVAILABLE = True
    except ImportError:
        CRYPTO_AVAILABLE = False

class CryptoManager:
    """
    Advanced cryptography manager for steganography operations
    """
    
    def __init__(self):
        if not CRYPTO_AVAILABLE:
            raise ImportError("PyCryptodome is not installed. Run: pip install pycryptodome")
        
        self.supported_algorithms = ['AES-256-GCM', 'AES-256-CBC']
    
    def encrypt(self, data: bytes, password: str, algorithm: str = 'AES-256-GCM') -> bytes:
        """
        Encrypt data with password-derived key
        """
        # Derive key from password
        key = self._derive_key(password, 32)
        
        if algorithm == 'AES-256-GCM':
            return self._encrypt_aes_gcm(data, key)
        else:
            return self._encrypt_aes_cbc(data, key)
    
    def decrypt(self, encrypted_data: bytes, password: str, 
                algorithm: str = 'AES-256-GCM') -> bytes:
        """
        Decrypt data with password
        """
        key = self._derive_key(password, 32)
        
        if algorithm == 'AES-256-GCM':
            return self._decrypt_aes_gcm(encrypted_data, key)
        else:
            return self._decrypt_aes_cbc(encrypted_data, key)
    
    def _encrypt_aes_gcm(self, data: bytes, key: bytes) -> bytes:
        """Encrypt using AES-GCM mode"""
        # Generate random IV
        iv = get_random_bytes(12)
        
        # Create cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        
        # Encrypt and get tag
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # Return IV + tag + ciphertext
        return iv + tag + ciphertext
    
    def _decrypt_aes_gcm(self, encrypted_data: bytes, key: bytes) -> bytes:
        """Decrypt AES-GCM encrypted data"""
        try:
            # Extract components
            iv = encrypted_data[:12]
            tag = encrypted_data[12:28]
            ciphertext = encrypted_data[28:]
            
            # Create cipher and decrypt
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            
            return decrypted_data
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def _encrypt_aes_cbc(self, data: bytes, key: bytes) -> bytes:
        """Encrypt using AES-CBC mode"""
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Pad data to block size
        padded_data = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        
        return iv + ciphertext
    
    def _decrypt_aes_cbc(self, encrypted_data: bytes, key: bytes) -> bytes:
        """Decrypt AES-CBC encrypted data"""
        try:
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(ciphertext)
            decrypted_data = unpad(decrypted_padded, AES.block_size)
            
            return decrypted_data
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def _derive_key(self, password: str, key_length: int) -> bytes:
        """
        Derive encryption key from password using PBKDF2
        """
        # Use fixed salt for consistency
        salt = b'steganoguard_salt_2024'
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,  # Iterations
            key_length
        )
        return key
    
    def generate_secure_password(self, length: int = 16) -> str:
        """
        Generate cryptographically secure random password
        """
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def calculate_hash(self, data: bytes, algorithm: str = 'sha256') -> str:
        """
        Calculate hash of data
        """
        hash_func = getattr(hashlib, algorithm)()
        hash_func.update(data)
        return hash_func.hexdigest()