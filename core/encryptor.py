from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path
from core.alert import log_event

def encrypt_file(file_path: str, key: bytes) -> dict:
    """
    Encrypts a file and replaces it with a .enc version.
    """
    path = Path(file_path).resolve()
    if not path.is_file():
        return {"status": "error", "message": "File not found."}

    try:
        cipher = Fernet(key)
        
        # Read original data
        with path.open("rb") as f:
            data = f.read()
            
        # Encrypt
        encrypted_data = cipher.encrypt(data)
        
        # Write to .enc file (e.g., data.txt -> data.txt.enc)
        enc_path = path.with_suffix(path.suffix + ".enc")
        with enc_path.open("wb") as f:
            f.write(encrypted_data)
            
        # Security step: Remove the original unencrypted file
        path.unlink()
        
        log_event("info", f"File successfully encrypted: {path.name}")
        return {
            "status": "success", 
            "message": f"Secured as {enc_path.name}",
            "enc_path": str(enc_path)
        }
    except Exception as e:
        log_event("error", f"Encryption failed for {path.name}: {str(e)}")
        return {"status": "error", "message": f"Encryption failed: {str(e)}"}

def decrypt_file(enc_path: str, key: bytes) -> dict:
    """
    Decrypts a .enc file. 
    Catches InvalidToken specifically to identify wrong passwords.
    """
    path = Path(enc_path).resolve()
    if not path.exists():
        return {"status": "error", "message": "Encrypted file not found."}

    try:
        cipher = Fernet(key)
        
        with path.open("rb") as f:
            encrypted_data = f.read()
            
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Restore original name (data.txt.enc -> data.txt)
        original_path = path.with_suffix('') 
        with original_path.open("wb") as f:
            f.write(decrypted_data)
            
        # Remove the encrypted version
        path.unlink() 
        
        log_event("info", f"File successfully decrypted: {original_path.name}")
        return {
            "status": "success", 
            "message": f"Decrypted: {original_path.name}",
            "original_path": str(original_path)
        }
    except InvalidToken:
        log_event("warning", f"Unauthorized access attempt (wrong password) for {path.name}")
        return {"status": "error", "message": "Access Denied: Incorrect password."}
    except Exception as e:
        log_event("error", f"Decryption failure: {str(e)}")
        return {"status": "error", "message": f"Decryption failed: {str(e)}"}