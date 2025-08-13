#!/usr/bin/env python3
"""
Targeted Ransomware Decryption Tool
Modified version for folder-specific decryption with improved stability
"""

import os
import sys
import time
import json
import logging
import argparse
from pathlib import Path
from base64 import b64decode
from datetime import datetime
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from Crypto.Cipher import AES
except ImportError:
    print("ERROR: PyCrypto/PyCryptodome not installed. Please install with: pip install pycryptodome")
    sys.exit(1)

# Original ransomware identifiers
SECRET_KEY = "SXpbALf2gHKTD9oIZbSUag=="
UNIQUE_ID = "Z71UARTPV4WH"
FILE_EXTENSION = f".{UNIQUE_ID}.sil3ncer"

class TargetedDecryptor:
    def __init__(self, secret_key=SECRET_KEY, unique_id=UNIQUE_ID, log_file=None):
        self.secret_key = secret_key
        self.unique_id = unique_id
        self.file_extension = f".{unique_id}.sil3ncer"
        self.processed_files = []
        self.failed_files = []
        self.progress_file = "decryption_progress.json"
        
        # Setup logging
        self.setup_logging(log_file)
        
        # Load previous progress if exists
        self.load_progress()
    
    def setup_logging(self, log_file=None):
        """Setup logging configuration"""
        if log_file is None:
            log_file = f"decrypt_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Targeted Decryptor initialized")
    
    def load_progress(self):
        """Load previous decryption progress"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    self.processed_files = data.get('processed_files', [])
                    self.failed_files = data.get('failed_files', [])
                self.logger.info(f"Loaded progress: {len(self.processed_files)} processed, {len(self.failed_files)} failed")
        except Exception as e:
            self.logger.warning(f"Could not load progress file: {e}")
    
    def save_progress(self):
        """Save current decryption progress"""
        try:
            progress_data = {
                'timestamp': datetime.now().isoformat(),
                'processed_files': self.processed_files,
                'failed_files': self.failed_files
            }
            with open(self.progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save progress: {e}")
    
    def find_encrypted_files(self, target_path):
        """Find encrypted files in specific directory"""
        encrypted_files = []
        target_path = Path(target_path)
        
        if not target_path.exists():
            self.logger.error(f"Target path does not exist: {target_path}")
            return encrypted_files
        
        self.logger.info(f"Scanning directory: {target_path}")
        
        try:
            # Use iterdir for better performance and error handling
            if target_path.is_file():
                if str(target_path).endswith(self.file_extension):
                    encrypted_files.append(str(target_path))
            else:
                for item in target_path.rglob(f"*{self.file_extension}"):
                    if item.is_file():
                        file_path = str(item)
                        if file_path not in self.processed_files:
                            encrypted_files.append(file_path)
                            
        except PermissionError as e:
            self.logger.warning(f"Permission denied accessing {target_path}: {e}")
        except Exception as e:
            self.logger.error(f"Error scanning {target_path}: {e}")
        
        self.logger.info(f"Found {len(encrypted_files)} encrypted files to process")
        return encrypted_files
    
    def decrypt_single_file(self, filename, chunksize=65536):
        """Decrypt a single file with improved error handling"""
        try:
            if filename in self.processed_files:
                self.logger.info(f"Skipping already processed file: {filename}")
                return True
                
            if not os.path.exists(filename):
                self.logger.warning(f"File not found: {filename}")
                return False
            
            output_file = filename.replace(self.file_extension, "")
            
            # Check if output file already exists
            if os.path.exists(output_file):
                self.logger.warning(f"Output file already exists: {output_file}")
                backup_name = f"{output_file}.backup_{int(time.time())}"
                os.rename(output_file, backup_name)
                self.logger.info(f"Existing file backed up as: {backup_name}")
            
            self.logger.info(f"Decrypting: {filename}")
            
            with open(filename, "rb") as infile:
                # Read original file size (first 16 bytes)
                size_data = infile.read(16)
                if len(size_data) != 16:
                    raise ValueError("Invalid file format: cannot read file size")
                
                try:
                    original_filesize = int(size_data.strip())
                except ValueError:
                    raise ValueError("Invalid file format: corrupted file size data")
                
                # Read IV (next 16 bytes)
                IV = infile.read(16)
                if len(IV) != 16:
                    raise ValueError("Invalid file format: cannot read IV")
                
                # Create decryptor
                try:
                    decryptor = AES.new(b64decode(self.secret_key), AES.MODE_CBC, IV)
                except Exception as e:
                    raise ValueError(f"Failed to create decryptor: {e}")
                
                # Decrypt file
                with open(output_file, "wb") as outfile:
                    bytes_written = 0
                    while True:
                        chunk = infile.read(chunksize)
                        if len(chunk) == 0:
                            break
                        
                        decrypted_chunk = decryptor.decrypt(chunk)
                        outfile.write(decrypted_chunk)
                        bytes_written += len(decrypted_chunk)
                    
                    # Truncate to original file size
                    if bytes_written > original_filesize:
                        outfile.truncate(original_filesize)
            
            # Verify decryption success
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                # Only remove encrypted file if decryption was successful
                os.remove(filename)
                self.processed_files.append(filename)
                self.logger.info(f"Successfully decrypted: {output_file}")
                return True
            else:
                raise ValueError("Decryption failed: output file is empty or missing")
                
        except Exception as e:
            self.logger.error(f"Failed to decrypt {filename}: {e}")
            self.failed_files.append(filename)
            
            # Clean up partial output file if it exists
            output_file = filename.replace(self.file_extension, "")
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                    self.logger.info(f"Cleaned up partial file: {output_file}")
                except:
                    pass
            
            return False
    
    def decrypt_files_in_folder(self, folder_path, max_workers=None, batch_size=10):
        """Decrypt all encrypted files in specified folder"""
        if max_workers is None:
            max_workers = min(4, cpu_count())  # Limit to 4 workers to prevent crashes
        
        encrypted_files = self.find_encrypted_files(folder_path)
        
        if not encrypted_files:
            self.logger.info("No encrypted files found to decrypt")
            return
        
        self.logger.info(f"Starting decryption of {len(encrypted_files)} files using {max_workers} workers")
        
        successful = 0
        failed = 0
        
        # Process files in batches to prevent memory issues
        for i in range(0, len(encrypted_files), batch_size):
            batch = encrypted_files[i:i + batch_size]
            self.logger.info(f"Processing batch {i//batch_size + 1}: files {i+1} to {min(i+batch_size, len(encrypted_files))}")
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit batch jobs
                future_to_file = {
                    executor.submit(self.decrypt_single_file, filename): filename 
                    for filename in batch
                }
                
                # Process results
                for future in as_completed(future_to_file):
                    filename = future_to_file[future]
                    try:
                        result = future.result(timeout=300)  # 5 minute timeout per file
                        if result:
                            successful += 1
                        else:
                            failed += 1
                    except Exception as e:
                        self.logger.error(f"Worker error for {filename}: {e}")
                        failed += 1
                    
                    # Save progress after each file
                    self.save_progress()
                    
                    # Progress update
                    total_processed = successful + failed
                    progress = (total_processed / len(encrypted_files)) * 100
                    self.logger.info(f"Progress: {progress:.1f}% ({total_processed}/{len(encrypted_files)}) - Success: {successful}, Failed: {failed}")
            
            # Small delay between batches to prevent system overload
            time.sleep(1)
        
        self.logger.info(f"Decryption completed! Success: {successful}, Failed: {failed}")
        
        if self.failed_files:
            self.logger.warning("Failed files:")
            for failed_file in self.failed_files:
                self.logger.warning(f"  - {failed_file}")
    
    def get_summary(self):
        """Get decryption summary"""
        return {
            'total_processed': len(self.processed_files),
            'total_failed': len(self.failed_files),
            'processed_files': self.processed_files,
            'failed_files': self.failed_files
        }

def main():
    parser = argparse.ArgumentParser(description='Targeted Ransomware Decryption Tool')
    parser.add_argument('target_path', help='Target folder or file path to decrypt')
    parser.add_argument('--workers', type=int, default=None, help='Number of worker threads (default: auto)')
    parser.add_argument('--batch-size', type=int, default=10, help='Batch size for processing (default: 10)')
    parser.add_argument('--log-file', default=None, help='Log file path (default: auto-generated)')
    parser.add_argument('--resume', action='store_true', help='Resume from previous session')
    
    args = parser.parse_args()
    
    # Initialize decryptor
    decryptor = TargetedDecryptor(log_file=args.log_file)
    
    if not args.resume:
        # Clear previous progress if not resuming
        decryptor.processed_files = []
        decryptor.failed_files = []
    
    try:
        # Start decryption
        decryptor.decrypt_files_in_folder(
            args.target_path, 
            max_workers=args.workers,
            batch_size=args.batch_size
        )
        
        # Print summary
        summary = decryptor.get_summary()
        print("\n" + "="*50)
        print("DECRYPTION SUMMARY")
        print("="*50)
        print(f"Total files processed: {summary['total_processed']}")
        print(f"Total files failed: {summary['total_failed']}")
        print(f"Success rate: {summary['total_processed']/(summary['total_processed']+summary['total_failed'])*100:.1f}%" if (summary['total_processed']+summary['total_failed']) > 0 else "No files processed")
        
    except KeyboardInterrupt:
        print("\nDecryption interrupted by user")
        decryptor.save_progress()
        print("Progress saved. Use --resume to continue later.")
    except Exception as e:
        print(f"Fatal error: {e}")
        decryptor.save_progress()
        sys.exit(1)

if __name__ == "__main__":
    main()