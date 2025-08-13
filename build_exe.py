#!/usr/bin/env python3
"""
Script to build standalone executables for the decryption tools
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run command and print output"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("SUCCESS")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    return run_command([sys.executable, "-m", "pip", "install", "-r", "requirements_decrypt.txt"])

def build_simple_exe():
    """Build simple decryptor executable"""
    print("\nBuilding simple_decrypt.exe...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "simple_decrypt",
        "--distpath", "dist",
        "--workpath", "build",
        "simple_decrypt.py"
    ]
    return run_command(cmd)

def build_targeted_exe():
    """Build targeted decryptor executable"""
    print("\nBuilding targeted_decrypt.exe...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "targeted_decrypt",
        "--distpath", "dist",
        "--workpath", "build",
        "targeted_decrypt.py"
    ]
    return run_command(cmd)

def main():
    print("Decryptor Executable Builder")
    print("="*30)
    
    # Check if we're in the right directory
    if not (Path("simple_decrypt.py").exists() and Path("targeted_decrypt.py").exists()):
        print("ERROR: Python scripts not found in current directory")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements")
        sys.exit(1)
    
    # Create output directory
    os.makedirs("dist", exist_ok=True)
    
    # Build executables
    success_count = 0
    
    if build_simple_exe():
        success_count += 1
        print("✓ simple_decrypt.exe built successfully")
    else:
        print("✗ Failed to build simple_decrypt.exe")
    
    if build_targeted_exe():
        success_count += 1
        print("✓ targeted_decrypt.exe built successfully")
    else:
        print("✗ Failed to build targeted_decrypt.exe")
    
    print(f"\nBuild complete: {success_count}/2 executables built")
    
    if success_count > 0:
        print("\nBuilt executables are in the 'dist' folder:")
        for exe_file in Path("dist").glob("*.exe"):
            size_mb = exe_file.stat().st_size / (1024*1024)
            print(f"  - {exe_file.name} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    main()