import json
import hashlib
from pathlib import Path
from core.alert import log_event

DB_DIR = Path("data")
DB_FILE = DB_DIR / "file_db.json"
SIG_FILE = DB_DIR / ".db.sig"  # <--- NEW: Hidden signature file

def _generate_db_signature(data: dict) -> str:
    """
    Creates a SHA-256 signature of the database content.
    sort_keys=True is critical to ensure the same dictionary always 
    produces the same hash string.
    """
    db_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(db_string.encode()).hexdigest()

def verify_storage_integrity() -> bool:
    """
    Checks if the database has been tampered with since last use.
    Should be called when the program starts.
    """
    if not DB_FILE.exists():
        return True  # No database yet is considered safe
    
    if not SIG_FILE.exists():
        log_event("critical", "DATABASE TAMPERING DETECTED: Missing signature file!")
        return False
    
    current_db = _load_db()
    stored_sig = SIG_FILE.read_text().strip()
    calculated_sig = _generate_db_signature(current_db)
    
    if calculated_sig == stored_sig:
        return True
    
    log_event("critical", "DATABASE TAMPERING DETECTED: Master Hash Mismatch!")
    return False

def _load_db() -> dict:
    if not DB_FILE.exists():
        return {}
    try:
        with DB_FILE.open("r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log_event("error", f"Database Read Error: {e}")
        return {}

def _save_db(data: dict) -> bool:
    """
    Saves the database AND updates the integrity signature.
    """
    try:
        DB_DIR.mkdir(exist_ok=True)
        # 1. Save the JSON data
        with DB_FILE.open("w") as f:
            json.dump(data, f, indent=4)
        
        # 2. Generate and save the new signature
        new_sig = _generate_db_signature(data)
        SIG_FILE.write_text(new_sig)
        
        return True
    except IOError as e:
        log_event("error", f"Database Write Error: {e}")
        return False

def store_file_metadata(file_path: str, salt_str: str, file_hash: str) -> dict:
    file_name = Path(file_path).name
    db = _load_db()
    
    db[file_name] = {
        "salt": salt_str,
        "hash": file_hash
    }
    
    if _save_db(db):
        log_event("info", f"Metadata updated for {file_name}")
        return {"status": "success", "message": f"Metadata saved for {file_name}"}
    
    return {"status": "error", "message": "Failed to update security database."}

def get_file_metadata(file_path: str) -> dict:
    file_name = Path(file_path).name
    db = _load_db()
    return db.get(file_name)

def remove_file_metadata(file_path: str):
    file_name = Path(file_path).name
    db = _load_db()
    if file_name in db:
        del db[file_name]
        if _save_db(db):
            log_event("info", f"Security record removed for {file_name}")