#!/usr/bin/env python3
"""
Script to build Windows executables using PyInstaller
Run this on a Windows machine with Python and PyInstaller installed
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
    return run_command([sys.executable, "-m", "pip", "install", "pycryptodome", "pyinstaller"])

def build_simple_exe():
    """Build simple decryptor executable for Windows"""
    print("\nBuilding simple_decrypt.exe for Windows...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "simple_decrypt",
        "--distpath", "windows_dist",
        "--workpath", "windows_build",
        "--clean",
        "simple_decrypt.py"
    ]
    return run_command(cmd)

def build_targeted_exe():
    """Build targeted decryptor executable for Windows"""
    print("\nBuilding targeted_decrypt.exe for Windows...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console", 
        "--name", "targeted_decrypt",
        "--distpath", "windows_dist",
        "--workpath", "windows_build",
        "--clean",
        "targeted_decrypt.py"
    ]
    return run_command(cmd)

def main():
    print("Windows Decryptor Executable Builder")
    print("="*40)
    print("NOTE: This script should be run on a Windows machine")
    print("      with Python 3.8+ and internet connection")
    print()
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("WARNING: This script is designed for Windows")
        print("The executables may not work properly on other platforms")
        print()
    
    # Check if we're in the right directory
    if not (Path("simple_decrypt.py").exists() and Path("targeted_decrypt.py").exists()):
        print("ERROR: Python scripts not found in current directory")
        print("Make sure simple_decrypt.py and targeted_decrypt.py are present")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements")
        sys.exit(1)
    
    # Create output directory
    os.makedirs("windows_dist", exist_ok=True)
    
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
        print("\nBuilt Windows executables are in the 'windows_dist' folder:")
        dist_path = Path("windows_dist")
        if dist_path.exists():
            for exe_file in dist_path.glob("*.exe"):
                try:
                    size_mb = exe_file.stat().st_size / (1024*1024)
                    print(f"  - {exe_file.name} ({size_mb:.1f} MB)")
                except:
                    print(f"  - {exe_file.name}")

    print("\nUsage Instructions:")
    print("1. Copy the .exe files to your target Windows machine")
    print("2. Open Command Prompt or PowerShell")
    print("3. Run: simple_decrypt.exe \"C:\\path\\to\\folder\"")
    print("   Or: targeted_decrypt.exe \"C:\\path\\to\\folder\" --workers 1")

if __name__ == "__main__":
    main()