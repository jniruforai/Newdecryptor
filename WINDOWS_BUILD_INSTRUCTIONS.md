# Building Windows Executables (.exe)

## Current Status
The executables I built are for Linux. To get Windows .exe files, you have two options:

## Option 1: Run Python Scripts Directly (Recommended)

### Requirements
- Windows machine with Python 3.8+ installed
- Install requirements: `pip install pycryptodome`

### Usage
```cmd
# Simple decryptor
python simple_decrypt.py "C:\path\to\encrypted\folder"

# Advanced decryptor  
python targeted_decrypt.py "C:\path\to\encrypted\folder" --workers 1 --batch-size 5
```

## Option 2: Build Windows .exe Files

### On a Windows Machine:

1. **Copy these files to Windows machine:**
   - `simple_decrypt.py`
   - `targeted_decrypt.py` 
   - `build_windows_exe.py`

2. **Install Python and requirements:**
   ```cmd
   pip install pycryptodome pyinstaller
   ```

3. **Build executables:**
   ```cmd
   python build_windows_exe.py
   ```

4. **Find your .exe files in:**
   ```
   windows_dist/
   ├── simple_decrypt.exe
   └── targeted_decrypt.exe
   ```

### Alternative: Using online build services
You can also use GitHub Actions or other CI/CD services to build Windows executables from the Python scripts.

## Ready-to-Use Files

### Python Scripts (Work on any OS)
✅ `simple_decrypt.py` - Ready to use with `python simple_decrypt.py "folder_path"`
✅ `targeted_decrypt.py` - Ready to use with `python targeted_decrypt.py "folder_path"`

### Linux Executables (If needed)
✅ `dist/simple_decrypt` - Linux executable
✅ `dist/targeted_decrypt` - Linux executable

## Quick Start for Windows

**Method 1: Direct Python (Easiest)**
```cmd
# Install requirements
pip install pycryptodome

# Use simple version
python simple_decrypt.py "C:\Users\YourName\Documents"

# Use advanced version
python targeted_decrypt.py "C:\Users\YourName\Documents" --workers 1
```

**Method 2: Build .exe then use**
```cmd
# After building with build_windows_exe.py
simple_decrypt.exe "C:\Users\YourName\Documents"
targeted_decrypt.exe "C:\Users\YourName\Documents" --workers 1
```

## Features Available in Both Versions

### Simple Decryptor
- ✅ Folder-specific targeting (no system-wide scanning)
- ✅ Progress display
- ✅ Automatic backup of existing files
- ✅ Error handling to prevent crashes
- ✅ File verification before cleanup

### Advanced Decryptor  
- ✅ All simple decryptor features PLUS:
- ✅ Detailed logging
- ✅ Progress saving and resume capability
- ✅ Configurable worker threads
- ✅ Batch processing
- ✅ Command-line options
- ✅ JSON progress tracking

## Example Usage Scenarios

### Test Recovery (Start Here)
```cmd
python simple_decrypt.py "C:\Users\Documents\TestFolder"
```

### Large Folder Recovery (Conservative)
```cmd  
python targeted_decrypt.py "C:\Data" --workers 1 --batch-size 3
```

### Resume Interrupted Recovery
```cmd
python targeted_decrypt.py "C:\Data" --resume
```

### Multiple Folder Recovery
```cmd
python targeted_decrypt.py "C:\Users\Documents" --workers 2
python targeted_decrypt.py "C:\Users\Pictures" --workers 1  
python targeted_decrypt.py "C:\Users\Videos" --workers 1
```

Both approaches will give you the same functionality - the Python scripts are just as effective as compiled executables!