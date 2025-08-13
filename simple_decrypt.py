#!/usr/bin/env python3
"""
Simple Targeted Decryptor
Easy-to-use version with minimal dependencies
"""

import os
import sys
import time
from pathlib import Path
from base64 import b64decode

try:
    from Crypto.Cipher import AES
except ImportError:
    print("ERROR: PyCrypto/PyCryptodome not installed.")
    print("Please install with: pip install pycryptodome")
    sys.exit(1)

# Original ransomware configuration
SECRET_KEY = "SXpbALf2gHKTD9oIZbSUag=="
UNIQUE_ID = "Z71UARTPV4WH"
FILE_EXTENSION = f".{UNIQUE_ID}.sil3ncer"

class SimpleDecryptor:
    def __init__(self):
        self.processed = 0
        self.failed = 0
        self.start_time = time.time()
    
    def find_encrypted_files(self, folder_path):
        """Find all encrypted files in folder"""
        encrypted_files = []
        folder = Path(folder_path)
        
        if not folder.exists():
            print(f"ERROR: Folder does not exist: {folder_path}")
            return []
        
        print(f"Scanning folder: {folder_path}")
        
        try:
            for file_path in folder.rglob(f"*{FILE_EXTENSION}"):
                if file_path.is_file():
                    encrypted_files.append(str(file_path))
        except Exception as e:
            print(f"Error scanning folder: {e}")
        
        print(f"Found {len(encrypted_files)} encrypted files")
        return encrypted_files
    
    def decrypt_file(self, filename):
        """Decrypt single file"""
        try:
            print(f"Decrypting: {os.path.basename(filename)}")
            
            output_file = filename.replace(FILE_EXTENSION, "")
            
            # Check if output already exists
            if os.path.exists(output_file):
                backup = f"{output_file}.backup_{int(time.time())}"
                os.rename(output_file, backup)
                print(f"  Existing file backed up as: {os.path.basename(backup)}")
            
            with open(filename, "rb") as infile:
                # Read file size
                size_data = infile.read(16)
                original_filesize = int(size_data.strip())
                
                # Read IV
                IV = infile.read(16)
                
                # Create decryptor
                decryptor = AES.new(b64decode(SECRET_KEY), AES.MODE_CBC, IV)
                
                # Decrypt
                with open(output_file, "wb") as outfile:
                    while True:
                        chunk = infile.read(65536)  # 64KB chunks
                        if not chunk:
                            break
                        outfile.write(decryptor.decrypt(chunk))
                    
                    outfile.truncate(original_filesize)
            
            # Verify and cleanup
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                os.remove(filename)
                print(f"  ✓ SUCCESS: {os.path.basename(output_file)}")
                self.processed += 1
                return True
            else:
                print(f"  ✗ FAILED: Output file invalid")
                if os.path.exists(output_file):
                    os.remove(output_file)
                self.failed += 1
                return False
                
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            self.failed += 1
            return False
    
    def decrypt_folder(self, folder_path):
        """Decrypt all files in folder"""
        files = self.find_encrypted_files(folder_path)
        
        if not files:
            print("No encrypted files found!")
            return
        
        print(f"\nStarting decryption of {len(files)} files...")
        print("-" * 50)
        
        for i, filename in enumerate(files, 1):
            print(f"[{i}/{len(files)}] ", end="")
            self.decrypt_file(filename)
            
            # Progress update every 10 files
            if i % 10 == 0:
                elapsed = time.time() - self.start_time
                rate = i / elapsed if elapsed > 0 else 0
                print(f"  Progress: {i}/{len(files)} ({i/len(files)*100:.1f}%) - {rate:.1f} files/sec")
        
        # Final summary
        elapsed = time.time() - self.start_time
        print("\n" + "="*50)
        print("DECRYPTION COMPLETE")
        print("="*50)
        print(f"Processed: {self.processed}")
        print(f"Failed: {self.failed}")
        print(f"Time: {elapsed:.1f} seconds")
        print(f"Rate: {(self.processed + self.failed)/elapsed:.1f} files/sec")

def main():
    if len(sys.argv) != 2:
        print("Usage: python simple_decrypt.py <folder_path>")
        print("\nExample:")
        print("  python simple_decrypt.py C:\\Users\\Documents")
        print("  python simple_decrypt.py /home/user/documents")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    print("Simple Ransomware Decryptor")
    print("="*30)
    print(f"Target folder: {folder_path}")
    print(f"Looking for: *{FILE_EXTENSION}")
    print()
    
    # Confirm before starting
    response = input("Start decryption? (y/N): ").lower()
    if response != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    decryptor = SimpleDecryptor()
    decryptor.decrypt_folder(folder_path)

if __name__ == "__main__":
    main()