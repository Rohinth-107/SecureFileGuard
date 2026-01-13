import hashlib
from pathlib import Path
from core.alert import log_event  # <--- NEW

def generate_hash(file_path):
    sha256 = hashlib.sha256()
    target_path = Path(file_path).resolve()

    if not target_path.is_file():
        return {'status': 'error', 'hash': None, 'message': f"File not found: {target_path}"}

    try:
        with target_path.open("rb") as f:
            while chunk := f.read(131072): 
                sha256.update(chunk)
        
        # --- LOG HASH GENERATION ---
        log_event("info", f"SHA-256 hash generated for {target_path.name}")
        return {'status': 'success', 'hash': sha256.hexdigest(), 'message': f"Hash generated."}
    
    except Exception as e:
        log_event("error", f"Hash generation failed for {target_path.name}: {str(e)}")
        return {'status': 'error', 'hash': None, 'message': str(e)}

def verify_file(file_path, expected_hash):
    result = generate_hash(file_path)
    file_name = Path(file_path).name
    
    if result['status'] == 'error':
        return False, result['message']
        
    if result['hash'] == expected_hash:
        # --- LOG PASS ---
        log_event("info", f"Integrity check passed for {file_name}")
        return True, f"Integrity Intact: {file_name}"
    else:
        # --- LOG SECURITY ALERT ---
        log_event("critical", f"INTEGRITY BREACH DETECTED: {file_name} has been modified!")
        return False, f"SECURITY ALERT: {file_name} hash mismatch!"