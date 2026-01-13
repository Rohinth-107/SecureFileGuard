import shutil
from pathlib import Path
from datetime import datetime
from core.alert import log_event

# Using a dot prefix makes it 'hidden' on most systems
BACKUP_DIR = Path(".backups")

def create_backup(file_path):
    """
    Creates a timestamped versioned backup of the file.
    Example: data.txt -> .backups/data.txt.20260113_183005.bak
    """
    try:
        source = Path(file_path).resolve()
        if not source.is_file():
            return {"status": "error", "message": f"Source '{source.name}' not found.", "backup_path": None}

        BACKUP_DIR.mkdir(exist_ok=True)
        
        # --- IMPROVEMENT: TIMESTAMPED VERSIONING ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = BACKUP_DIR / f"{source.name}.{timestamp}.bak"

        # Perform the copy
        shutil.copy2(source, dest)

        # Verification
        if dest.exists() and dest.stat().st_size == source.stat().st_size:
            log_event("info", f"Versioned backup created: {dest.name}")
            return {
                "status": "success", 
                "message": f"Backup version {timestamp} verified.", 
                "backup_path": str(dest)
            }
        else:
            log_event("error", f"Backup size mismatch for {source.name}")
            return {"status": "error", "message": "Backup created but size mismatch detected!", "backup_path": None}

    except Exception as e:
        log_event("critical", f"Backup failed for {file_path}: {str(e)}")
        return {"status": "error", "message": f"Critical Backup Failure: {str(e)}", "backup_path": None}

def restore_backup(file_path):
    """
    Automatically finds and restores the LATEST versioned backup for a file.
    """
    try:
        target = Path(file_path).resolve()
        
        # --- IMPROVEMENT: FIND LATEST VERSION ---
        # Search for all files matching "filename.*.bak"
        backups = sorted(BACKUP_DIR.glob(f"{target.name}.*.bak"))
        
        if not backups:
            log_event("warning", f"Restore attempted but no backups found for {target.name}")
            return {"status": "error", "message": f"No backup versions found for '{target.name}'."}

        # Pick the last one in the sorted list (most recent timestamp)
        latest_backup = backups[-1]

        shutil.copy2(latest_backup, target)
        
        log_event("info", f"Restored latest version ({latest_backup.name}) to {target.name}")
        return {
            "status": "success", 
            "message": f"Restored successfully from version: {latest_backup.name}"
        }

    except Exception as e:
        log_event("error", f"Restore failed for {file_path}: {str(e)}")
        return {"status": "error", "message": f"Restore failed: {str(e)}"}

def list_versions(file_path):
    """Helper to list all available backup timestamps for a file."""
    target_name = Path(file_path).name
    backups = sorted(BACKUP_DIR.glob(f"{target_name}.*.bak"), reverse=True)
    return [b.name for b in backups]