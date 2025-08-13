# Targeted Decryption Tool - Usage Instructions

## Overview
These are improved, targeted versions of the ransomware decryption tool that avoid the issues with the original full-system scanner:

- **Crashes less frequently** - Better error handling and resource management
- **Targets specific folders** - No more full-system scanning
- **Progress tracking** - Resume interrupted decryptions
- **Batch processing** - Handles large numbers of files safely

## Files Included

### 1. `simple_decrypt.py` / `simple_decrypt.exe`
- **Best for**: Quick, straightforward decryption of a single folder
- **Features**: Minimal interface, easy to use
- **Usage**: `simple_decrypt.exe C:\path\to\folder`

### 2. `targeted_decrypt.py` / `targeted_decrypt.exe`
- **Best for**: Large-scale recovery with advanced features
- **Features**: Progress saving, resume capability, batch processing, detailed logging
- **Usage**: `targeted_decrypt.exe C:\path\to\folder [options]`

## Quick Start

### Option 1: Use Pre-built Executables
```cmd
# Simple version
simple_decrypt.exe "C:\Users\Documents"

# Advanced version
targeted_decrypt.exe "C:\Users\Documents" --workers 2 --batch-size 5
```

### Option 2: Run Python Scripts Directly
```cmd
# Install requirements first
pip install pycryptodome

# Simple version
python simple_decrypt.py "C:\Users\Documents"

# Advanced version
python targeted_decrypt.py "C:\Users\Documents"
```

## Detailed Usage

### Simple Decryptor

```cmd
simple_decrypt.exe <folder_path>
```

**Example:**
```cmd
simple_decrypt.exe "C:\Users\John\Documents"
```

**Features:**
- Scans specified folder (and subfolders) for encrypted files
- Decrypts files one by one with progress display
- Creates backups if decrypted files already exist
- Simple console output

### Targeted Decryptor (Advanced)

```cmd
targeted_decrypt.exe <folder_path> [options]
```

**Options:**
- `--workers N` - Number of parallel workers (default: 4, max recommended: 4)
- `--batch-size N` - Files to process per batch (default: 10)
- `--log-file FILE` - Custom log file path
- `--resume` - Resume from previous interrupted session

**Examples:**
```cmd
# Basic usage
targeted_decrypt.exe "C:\Users\Documents"

# Conservative settings (fewer crashes)
targeted_decrypt.exe "C:\Users\Documents" --workers 1 --batch-size 5

# Resume interrupted session
targeted_decrypt.exe "C:\Users\Documents" --resume

# Custom logging
targeted_decrypt.exe "C:\Users\Documents" --log-file "my_decrypt.log"
```

## Step-by-Step Recovery Strategy

### Phase 1: Test with Small Folder
```cmd
# Start with a small test folder
simple_decrypt.exe "C:\Users\Documents\TestFolder"
```

### Phase 2: Process Important Folders
```cmd
# Process critical folders one by one
targeted_decrypt.exe "C:\Users\Documents" --workers 2
targeted_decrypt.exe "C:\Users\Pictures" --workers 2
targeted_decrypt.exe "C:\Users\Videos" --workers 1
```

### Phase 3: Handle Large Directories
```cmd
# Use conservative settings for large folders
targeted_decrypt.exe "C:\Data" --workers 1 --batch-size 3
```

### Phase 4: Resume if Interrupted
```cmd
# If process crashes or is interrupted
targeted_decrypt.exe "C:\Data" --resume
```

## Troubleshooting

### If the Tool Crashes:
1. **Reduce workers**: Use `--workers 1`
2. **Reduce batch size**: Use `--batch-size 1`
3. **Use resume**: Add `--resume` to continue from where it stopped
4. **Check logs**: Look at the generated log files for error details

### If Files Are Not Decrypting:
1. **Check file extension**: Files must end with `.Z71UARTPV4WH.sil3ncer`
2. **Check permissions**: Ensure you have write access to the folder
3. **Check disk space**: Ensure enough free space for decrypted files
4. **Verify file integrity**: Corrupted encrypted files cannot be decrypted

### Performance Tips:
- **SSDs**: Can handle more workers (up to 4)
- **HDDs**: Use 1-2 workers maximum
- **Low RAM**: Reduce batch size to 3-5
- **High RAM**: Can use larger batch sizes (10-20)

## Progress Tracking

The advanced version creates these files:
- `decryption_progress.json` - Progress tracking (for resume)
- `decrypt_log_YYYYMMDD_HHMMSS.log` - Detailed logs
- Automatic backups of existing files

## Building Your Own Executable

If you want to create your own executable:

```cmd
# Install requirements
pip install -r requirements_decrypt.txt

# Build executables
python build_exe.py
```

This creates executables in the `dist/` folder.

## Safety Features

### Built-in Protections:
- **Backup existing files** before overwriting
- **Verify decryption success** before deleting encrypted files
- **Progress saving** to resume interrupted operations
- **Detailed logging** for troubleshooting
- **Resource limiting** to prevent system overload

### What the Tool Does NOT Do:
- Does not scan entire system (only specified folders)
- Does not modify registry or system files
- Does not connect to internet
- Does not require admin privileges (unless folder requires it)

## File Identification

The tool looks for files with this pattern:
```
original_filename.Z71UARTPV4WH.sil3ncer
```

After decryption, files are restored to:
```
original_filename
```

## Support

If you encounter issues:

1. **Check the log files** for detailed error messages
2. **Try with a small test folder** first
3. **Use conservative settings** (fewer workers, smaller batches)
4. **Ensure sufficient disk space** and permissions
5. **Consider running from Command Prompt as Administrator** if permission issues occur

Remember: The tool preserves encrypted files until decryption is successful, so your data remains safe during the process.