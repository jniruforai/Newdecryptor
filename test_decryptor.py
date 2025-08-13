#!/usr/bin/env python3
"""
Test script to verify the decryption tools work correctly
Creates sample encrypted files for testing
"""

import os
import tempfile
from pathlib import Path
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import subprocess
import sys

SECRET_KEY = "SXpbALf2gHKTD9oIZbSUag=="
UNIQUE_ID = "Z71UARTPV4WH"
FILE_EXTENSION = f".{UNIQUE_ID}.sil3ncer"

def create_test_file(content, filename):
    """Create a test file with given content"""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def encrypt_file_for_test(input_file, output_file):
    """Encrypt a file using the same method as the ransomware"""
    # Read original file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Generate random IV
    iv = get_random_bytes(16)
    
    # Create encryptor
    cipher = AES.new(b64decode(SECRET_KEY), AES.MODE_CBC, iv)
    
    # Pad data to 16-byte boundary
    pad_length = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_length] * pad_length)
    
    # Encrypt
    encrypted_data = cipher.encrypt(padded_data)
    
    # Write encrypted file with metadata
    with open(output_file, 'wb') as f:
        # Write original file size (16 bytes)
        f.write(str(len(data)).ljust(16, ' ').encode())
        # Write IV (16 bytes)
        f.write(iv)
        # Write encrypted data
        f.write(encrypted_data)
    
    print(f"Created test encrypted file: {output_file}")

def create_test_environment():
    """Create test environment with encrypted files"""
    test_dir = Path("test_environment")
    test_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (test_dir / "documents").mkdir(exist_ok=True)
    (test_dir / "pictures").mkdir(exist_ok=True)
    
    # Create test files
    test_files = [
        ("documents/test1.txt", "This is test document 1.\nMultiple lines of text here."),
        ("documents/test2.txt", "This is test document 2 with different content."),
        ("pictures/readme.txt", "This folder contains picture files."),
        ("root_file.txt", "This is a file in the root test directory."),
    ]
    
    created_files = []
    for relative_path, content in test_files:
        file_path = test_dir / relative_path
        create_test_file(content, file_path)
        
        # Create encrypted version
        encrypted_path = str(file_path) + FILE_EXTENSION
        encrypt_file_for_test(file_path, encrypted_path)
        
        # Remove original (simulate ransomware)
        file_path.unlink()
        
        created_files.append(encrypted_path)
    
    print(f"\nTest environment created in: {test_dir}")
    print(f"Created {len(created_files)} encrypted files")
    return test_dir

def test_simple_decryptor(test_dir):
    """Test the simple decryptor"""
    print("\n" + "="*50)
    print("TESTING SIMPLE DECRYPTOR")
    print("="*50)
    
    try:
        # Run simple decryptor
        result = subprocess.run([
            sys.executable, "simple_decrypt.py", str(test_dir)
        ], input="y\n", text=True, capture_output=True, timeout=60)
        
        print("Return code:", result.returncode)
        print("Output:", result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Test timed out")
        return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False

def test_targeted_decryptor(test_dir):
    """Test the targeted decryptor"""
    print("\n" + "="*50)
    print("TESTING TARGETED DECRYPTOR")
    print("="*50)
    
    try:
        # Run targeted decryptor
        result = subprocess.run([
            sys.executable, "targeted_decrypt.py", str(test_dir), 
            "--workers", "1", "--batch-size", "2"
        ], capture_output=True, text=True, timeout=60)
        
        print("Return code:", result.returncode)
        print("Output:", result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Test timed out")
        return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False

def verify_decryption(test_dir):
    """Verify that files were decrypted correctly"""
    print("\n" + "="*50)
    print("VERIFYING DECRYPTION RESULTS")
    print("="*50)
    
    # Check for decrypted files
    decrypted_files = list(Path(test_dir).rglob("*.txt"))
    encrypted_files = list(Path(test_dir).rglob(f"*{FILE_EXTENSION}"))
    
    print(f"Decrypted files found: {len(decrypted_files)}")
    print(f"Encrypted files remaining: {len(encrypted_files)}")
    
    # Verify content
    expected_content = {
        "test1.txt": "This is test document 1.\nMultiple lines of text here.",
        "test2.txt": "This is test document 2 with different content.",
        "readme.txt": "This folder contains picture files.",
        "root_file.txt": "This is a file in the root test directory.",
    }
    
    success_count = 0
    for file_path in decrypted_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            filename = file_path.name
            if filename in expected_content:
                if content == expected_content[filename]:
                    print(f"✓ {filename}: Content verified")
                    success_count += 1
                else:
                    print(f"✗ {filename}: Content mismatch")
            else:
                print(f"? {filename}: Unexpected file")
        except Exception as e:
            print(f"✗ {filename}: Error reading - {e}")
    
    return success_count == len(expected_content)

def cleanup_test_environment():
    """Clean up test files"""
    import shutil
    try:
        shutil.rmtree("test_environment")
        print("Test environment cleaned up")
    except:
        pass

def main():
    print("Decryptor Testing Script")
    print("="*30)
    
    # Check dependencies
    try:
        from Crypto.Cipher import AES
        print("✓ PyCrypto/PyCryptodome available")
    except ImportError:
        print("✗ PyCrypto/PyCryptodome not available")
        print("Install with: pip install pycryptodome")
        return False
    
    # Check if scripts exist
    if not (Path("simple_decrypt.py").exists() and Path("targeted_decrypt.py").exists()):
        print("✗ Decryptor scripts not found")
        return False
    
    print("✓ All dependencies found")
    
    try:
        # Create test environment
        test_dir = create_test_environment()
        
        # Test simple decryptor (recreate environment for second test)
        cleanup_test_environment()
        test_dir = create_test_environment()
        simple_success = test_simple_decryptor(test_dir)
        verify_simple = verify_decryption(test_dir)
        
        # Test targeted decryptor (recreate environment for second test)
        cleanup_test_environment()
        test_dir = create_test_environment()
        targeted_success = test_targeted_decryptor(test_dir)
        verify_targeted = verify_decryption(test_dir)
        
        # Results
        print("\n" + "="*50)
        print("TEST RESULTS")
        print("="*50)
        print(f"Simple decryptor: {'✓ PASS' if simple_success and verify_simple else '✗ FAIL'}")
        print(f"Targeted decryptor: {'✓ PASS' if targeted_success and verify_targeted else '✗ FAIL'}")
        
        overall_success = simple_success and verify_simple and targeted_success and verify_targeted
        print(f"\nOverall: {'✓ ALL TESTS PASSED' if overall_success else '✗ SOME TESTS FAILED'}")
        
        return overall_success
        
    finally:
        cleanup_test_environment()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)