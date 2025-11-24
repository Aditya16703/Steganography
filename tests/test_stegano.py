"""
Comprehensive test suite for SteganoGuard Pro
"""

import unittest
import os
import tempfile
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from core.stegano_engine import SteganoEngine
    from core.crypto_manager import CryptoManager
    from core.file_processor import FileProcessor
    from utils.validators import Validators
except ImportError:
    # Alternative import path
    from src.core.stegano_engine import SteganoEngine
    from src.core.crypto_manager import CryptoManager
    from src.core.file_processor import FileProcessor
    from src.utils.validators import Validators


class TestSteganoEngine(unittest.TestCase):
    """Test cases for SteganoEngine class"""
    
    def setUp(self):
        """Set up test environment"""
        self.stegano = SteganoEngine()
        self.test_data = b"Hello SteganoGuard Pro! Test message."
        self.test_password = "test_password_123"
        
        # Create temporary test image
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.temp_dir, "test_image.png")
        self._create_test_image()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_image(self, width=100, height=100):
        """Create a test PNG image for testing"""
        try:
            from PIL import Image
            import numpy as np
            
            # Create random image data
            img_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
            image = Image.fromarray(img_array)
            image.save(self.test_image_path, 'PNG')
        except ImportError:
            self.skipTest("PIL or numpy not available")
    
    def test_engine_initialization(self):
        """Test SteganoEngine initialization"""
        self.assertIsInstance(self.stegano, SteganoEngine)
        self.assertIn('LSB', self.stegano.techniques)
    
    def test_capacity_analysis(self):
        """Test image capacity analysis"""
        analysis = self.stegano.analyze_capacity(self.test_image_path)
        
        self.assertIn('image_info', analysis)
        self.assertIn('capacity_analysis', analysis)
        
        # Check capacity calculations
        capacity_1bit = analysis['capacity_analysis']['1_bit_lsb']
        self.assertGreater(capacity_1bit['bytes'], 0)
    
    def test_data_embedding_extraction(self):
        """Test basic data embedding and extraction"""
        # Embed data
        stego_array, metadata = self.stegano.embed_data_secure(
            self.test_image_path,
            self.test_data,
            bits=2
        )
        
        # Verify metadata
        self.assertIn('embedding_info', metadata)
        self.assertEqual(metadata['data_info']['original_size'], len(self.test_data))
        
        # Save stego image temporarily
        from PIL import Image
        stego_image_path = os.path.join(self.temp_dir, "stego_image.png")
        Image.fromarray(stego_array).save(stego_image_path)
        
        # Extract data
        extracted_data, extraction_info = self.stegano.extract_data_secure(
            stego_image_path,
            bits=2
        )
        
        # Verify extraction
        self.assertEqual(self.test_data, extracted_data)
    
    def test_encrypted_embedding_extraction(self):
        """Test encrypted data embedding and extraction"""
        # Embed with encryption
        stego_array, metadata = self.stegano.embed_data_secure(
            self.test_image_path,
            self.test_data,
            password=self.test_password,
            bits=2
        )
        
        self.assertTrue(metadata['embedding_info']['password_used'])
        
        # Save stego image
        from PIL import Image
        stego_image_path = os.path.join(self.temp_dir, "encrypted_stego.png")
        Image.fromarray(stego_array).save(stego_image_path)
        
        # Extract with correct password
        extracted_data, extraction_info = self.stegano.extract_data_secure(
            stego_image_path,
            password=self.test_password,
            bits=2
        )
        
        self.assertEqual(self.test_data, extracted_data)
    
    def test_different_lsb_bits(self):
        """Test embedding with different LSB bits"""
        for bits in [1, 2]:
            with self.subTest(bits=bits):
                stego_array, metadata = self.stegano.embed_data_secure(
                    self.test_image_path,
                    self.test_data[:10],  # Small data for quick test
                    bits=bits
                )
                
                # Save and extract
                from PIL import Image
                stego_path = os.path.join(self.temp_dir, f"stego_{bits}bit.png")
                Image.fromarray(stego_array).save(stego_path)
                
                extracted_data, _ = self.stegano.extract_data_secure(
                    stego_path,
                    bits=bits
                )
                
                self.assertEqual(self.test_data[:10], extracted_data)


class TestCryptoManager(unittest.TestCase):
    """Test cases for CryptoManager class"""
    
    def setUp(self):
        self.crypto = CryptoManager()
        self.test_data = b"Secret data for encryption testing"
        self.test_password = "strong_password_123!"
    
    def test_encryption_decryption(self):
        """Test basic encryption and decryption"""
        # Encrypt
        encrypted = self.crypto.encrypt(self.test_data, self.test_password)
        
        # Verify encryption changed data
        self.assertNotEqual(self.test_data, encrypted)
        
        # Decrypt
        decrypted = self.crypto.decrypt(encrypted, self.test_password)
        
        # Verify original data recovered
        self.assertEqual(self.test_data, decrypted)
    
    def test_password_generation(self):
        """Test secure password generation"""
        password = self.crypto.generate_secure_password()
        
        # Check length
        self.assertEqual(len(password), 16)
    
    def test_hash_calculation(self):
        """Test hash calculation"""
        hash_value = self.crypto.calculate_hash(self.test_data)
        
        # Check hash format (SHA-256 should be 64 chars)
        self.assertEqual(len(hash_value), 64)
        
        # Verify consistency
        hash_value2 = self.crypto.calculate_hash(self.test_data)
        self.assertEqual(hash_value, hash_value2)


class TestFileProcessor(unittest.TestCase):
    """Test cases for FileProcessor class"""
    
    def setUp(self):
        self.processor = FileProcessor()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files
        self.test_image_path = os.path.join(self.temp_dir, "test.png")
        self._create_test_image()
    
    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_image(self, width=50, height=50):
        """Create a test image"""
        try:
            from PIL import Image
            import numpy as np
            
            img_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
            image = Image.fromarray(img_array)
            image.save(self.test_image_path, 'PNG')
        except ImportError:
            self.skipTest("PIL or numpy not available")
    
    def test_file_analysis(self):
        """Test file analysis functionality"""
        analysis = self.processor.analyze_file(self.test_image_path)
        
        # Check structure
        self.assertIn('basic_info', analysis)
        self.assertIn('security_info', analysis)
        
        # Check basic info
        self.assertEqual(analysis['basic_info']['filename'], 'test.png')
        self.assertEqual(analysis['basic_info']['extension'], '.png')
    
    def test_validation(self):
        """Test file validation"""
        # Valid file
        is_valid, message = self.processor.validate_file_for_steganography(self.test_image_path)
        self.assertTrue(is_valid)
        self.assertEqual(message, "File is valid")
        
        # Nonexistent file
        is_valid, message = self.processor.validate_file_for_steganography("nonexistent.png")
        self.assertFalse(is_valid)
        self.assertIn("does not exist", message)


class TestValidators(unittest.TestCase):
    """Test cases for Validators class"""
    
    def test_password_validation(self):
        """Test password validation"""
        # Valid password
        is_valid, message = Validators.validate_password("strongpass123")
        self.assertTrue(is_valid)
        
        # Empty password (allowed for no encryption)
        is_valid, message = Validators.validate_password("")
        self.assertTrue(is_valid)
        
        # Too short password
        is_valid, message = Validators.validate_password("123")
        self.assertFalse(is_valid)
        self.assertIn("at least 4 characters", message)
    
    def test_lsb_bits_validation(self):
        """Test LSB bits validation"""
        # Valid bits
        for bits in [1, 2, 3, 4]:
            is_valid, message = Validators.validate_lsb_bits(bits)
            self.assertTrue(is_valid)
        
        # Invalid bits
        for bits in [0, 5]:
            is_valid, message = Validators.validate_lsb_bits(bits)
            self.assertFalse(is_valid)


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSteganoEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestCryptoManager))
    suite.addTests(loader.loadTestsFromTestCase(TestFileProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestValidators))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)