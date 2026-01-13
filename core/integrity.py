import hashlib
from pathlib import Path

def generate_hash(file_path):
    """
    Generates a SHA-256 hash of a file.
    Handles absolute/relative paths and large files efficiently.
    
    Returns:
        dict: {
            'status': 'success' | 'error',
            'hash': str or None,
            'message': str
        }
    """
    sha256 = hashlib.sha256()
    target_path = Path(file_path).resolve() # Converts to absolute path for reliability

    if not target_path.is_file():
        return {
            'status': 'error',
            'hash': None,
            'message': f"File not found: {target_path}"
        }

    try:
        # 128KB buffer is often faster for modern hardware than 64KB
        with target_path.open("rb") as f:
            while chunk := f.read(131072): 
                sha256.update(chunk)
        
        return {
            'status': 'success',
            'hash': sha256.hexdigest(),
            'message': f"Hash generated for {target_path.name}"
        }
    
    except PermissionError:
        return {'status': 'error', 'hash': None, 'message': "Permission denied."}
    except Exception as e:
        return {'status': 'error', 'hash': None, 'message': str(e)}

def verify_file(file_path, expected_hash):
    """
    Verifies if a file matches the expected hash.
    """
    result = generate_hash(file_path)
    
    if result['status'] == 'error':
        return False, result['message']
        
    if result['hash'] == expected_hash:
        return True, f"Integrity Intact: {Path(file_path).name}"
    else:
        return False, f"SECURITY ALERT: {Path(file_path).name} hash mismatch!"