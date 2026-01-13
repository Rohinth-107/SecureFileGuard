import json
import hashlib
from core.alert import log_event
from core import config

def _generate_db_signature(data: dict) -> str:
    """Creates a SHA-256 signature of the database content."""
    # sort_keys=True ensures the hash is identical regardless of dict order
    db_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(db_string.encode()).hexdigest()

def verify_storage_integrity() -> bool:
    """Checks if the database has been tampered with since last use."""
    if not config.DB_FILE.exists():
        return True 
    
    if not config.SIG_FILE.exists():
        log_event("critical", "DATABASE TAMPERING: Signature file is missing!")
        return False
    
    current_db = _load_db()
    try:
        stored_sig = config.SIG_FILE.read_text().strip()
        calculated_sig = _generate_db_signature(current_db)
        
        if calculated_sig == stored_sig:
            log_event("info", "Database integrity verified.")
            return True
        
        log_event("critical", "DATABASE TAMPERING: Master signature mismatch!")
        return False
    except Exception as e:
        log_event("error", f"Integrity verification error: {e}")
        return False

def _load_db() -> dict:
    if not config.DB_FILE.exists():
        return {}
    try:
        with config.DB_FILE.open("r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log_event("error", f"Database Read Error: {e}")
        return {}

def _save_db(data: dict) -> bool:
    """Saves the database AND updates the signature file."""
    try:
        config.DATA_DIR.mkdir(exist_ok=True)
        # 1. Save data
        with config.DB_FILE.open("w") as f:
            json.dump(data, f, indent=4)
        
        # 2. Update signature
        new_sig = _generate_db_signature(data)
        config.SIG_FILE.write_text(new_sig)
        return True
    except Exception as e:
        log_event("error", f"Database Save Error: {e}")
        return False

def store_file_metadata(file_path: str, salt_str: str, file_hash: str) -> dict:
    from pathlib import Path
    file_name = Path(file_path).name
    db = _load_db()
    
    db[file_name] = {"salt": salt_str, "hash": file_hash}
    
    if _save_db(db):
        log_event("info", f"Metadata secured for {file_name}")
        return {"status": "success", "message": f"Metadata saved for {file_name}"}
    return {"status": "error", "message": "Storage update failed."}

def get_file_metadata(file_path: str) -> dict:
    from pathlib import Path
    file_name = Path(file_path).name
    return _load_db().get(file_name)

def remove_file_metadata(file_path: str):
    from pathlib import Path
    file_name = Path(file_path).name
    db = _load_db()
    if file_name in db:
        del db[file_name]
        _save_db(db)
        log_event("info", f"Metadata purged for {file_name}")