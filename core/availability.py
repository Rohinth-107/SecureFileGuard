import shutil
from pathlib import Path

# Using a dot prefix makes it 'hidden' on many systems
BACKUP_DIR = Path(".backups")

def create_backup(file_path):
    """
    Creates a secure backup and verifies its existence and size.
    """
    try:
        source = Path(file_path)
        if not source.exists():
            print(f"❌ Availability Error: Source file '{file_path}' not found.")
            return None

        BACKUP_DIR.mkdir(exist_ok=True)
        dest = BACKUP_DIR / f"{source.name}.bak"

        # Perform the copy
        shutil.copy2(source, dest)

        # FINAL IMPROVEMENT: Post-copy verification
        if dest.exists() and dest.stat().st_size == source.stat().st_size:
            print(f"✅ Availability: Verified backup created at {dest}")
            return str(dest)
        else:
            print("⚠️ Availability Warning: Backup created but size mismatch detected!")
            return None

    except Exception as e:
        print(f"⚠️ Availability Critical: Backup failed! {e}")
        return None

def restore_backup(file_path):
    """
    Overwrites a corrupted/lost file with its healthy backup.
    """
    target = Path(file_path)
    backup_path = BACKUP_DIR / f"{target.name}.bak"

    if not backup_path.exists():
        print(f"❌ Availability Error: No backup found for '{target.name}'.")
        return False

    try:
        shutil.copy2(backup_path, target)
        print(f"🔄 Availability: {target.name} has been restored successfully.")
        return True
    except Exception as e:
        print(f"⚠️ Availability Error: Restore failed: {e}")
        return False