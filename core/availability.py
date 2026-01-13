import shutil
from pathlib import Path

# Using a dot prefix makes it 'hidden' on most systems
BACKUP_DIR = Path(".backups")

def create_backup(file_path):
    """
    Creates a secure backup and verifies its existence and size.
    Returns: dict {status, message, backup_path}
    """
    try:
        source = Path(file_path).resolve()
        
        # Security Check: Ensure it's a file, not a folder
        if not source.is_file():
            return {
                "status": "error",
                "message": f"Source '{source.name}' is not a valid file.",
                "backup_path": None
            }

        BACKUP_DIR.mkdir(exist_ok=True)
        dest = BACKUP_DIR / f"{source.name}.bak"

        # Perform the copy (preserves metadata)
        shutil.copy2(source, dest)

        # Verification: Check if file exists and size matches
        if dest.exists() and dest.stat().st_size == source.stat().st_size:
            return {
                "status": "success",
                "message": f"Backup verified for {source.name}.",
                "backup_path": str(dest)
            }
        else:
            return {
                "status": "error",
                "message": "Backup created but size mismatch detected!",
                "backup_path": None
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Critical Backup Failure: {str(e)}",
            "backup_path": None
        }

def restore_backup(file_path):
    """
    Overwrites a corrupted/lost file with its healthy backup.
    Returns: dict {status, message}
    """
    try:
        target = Path(file_path).resolve()
        backup_path = BACKUP_DIR / f"{target.name}.bak"

        if not backup_path.exists():
            return {
                "status": "error",
                "message": f"No backup found for '{target.name}'."
            }

        # Restore the backup
        shutil.copy2(backup_path, target)
        
        return {
            "status": "success",
            "message": f"File '{target.name}' successfully restored from backup."
        }

    except PermissionError:
        return {
            "status": "error",
            "message": f"Permission denied: Ensure '{target.name}' is not open in another program."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Restore failed: {str(e)}"
        }