# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.11.13 (main, Jul 23 2025, 18:09:53) [GCC 12.2.0]
# Embedded file name: decrypt.py
import os
from base64 import b64decode
from Crypto.Cipher import AES
from multiprocessing import Pool, cpu_count
import win32api

class FileScanner:

    def __init__(self, secret_key, unique_id):
        self.all = []
        self.secret_key = secret_key
        self.unique_id = unique_id

    def get_path(self, drive_name):
        O = []
        for r, d, f in os.walk(drive_name):
            for filename in f:
                if filename.endswith(f".{self.unique_id}.sil3ncer"):
                    O.append(os.path.join(r, filename))
            else:
                return O

    def scan_drives(self):
        try:
            drives = [drive for drive in win32api.GetLogicalDriveStrings().split("\x00") if os.path.exists(drive)]
        except Exception as e:
            try:
                print(f"Error accessing drives: {e}")
                drives = []
            finally:
                e = None
                del e

        else:
            for D in reversed(drives):
                print(f"Scanning Drive {D} ...")
                self.all.extend(self.get_path(D))


class Decryptor(FileScanner):

    def __init__(self, secret_key, unique_id):
        super().__init__(secret_key, unique_id)

    def decrypt_file(self, filename, chunksize=65536):
        try:
            output_file = filename.replace(f".{self.unique_id}.sil3ncer", "")
            with open(filename, "rb") as infile:
                original_filesize = int(infile.read(16))
                IV = infile.read(16)
                decryptor = AES.new(b64decode(self.secret_key), AES.MODE_CBC, IV)
                with open(output_file, "wb") as outfile:
                    while True:
                        chunk = infile.read(chunksize)
                        if len(chunk) == 0:
                            break
                        outfile.write(decryptor.decrypt(chunk))

                    outfile.truncate(original_filesize)
            os.remove(filename)
        except Exception as e:
            try:
                pass
            finally:
                e = None
                del e

    def decrypt_files(self):
        self.scan_drives()
        total_files = len(self.all)
        if total_files == 0:
            print("No encrypted files found.")
            return
        with Pool(processes=(cpu_count())) as pool:
            for i, _ in enumerate(pool.imap_unordered(self.decrypt_file, self.all), 1):
                progress = i / total_files * 100
                print(f"Decryption Progress: {progress:.2f}% ({i}/{total_files})")


if __name__ == "__main__":
    secret_key = "SXpbALf2gHKTD9oIZbSUag=="
    unique_id = "Z71UARTPV4WH"
    decryptor = Decryptor(secret_key, unique_id)
    decryptor.decrypt_files()

# okay decompiling decrypt.exe_extracted/decrypt.pyc
