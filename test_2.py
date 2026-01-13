import os
import time
from core import availability, integrity, password, encryptor, storage, alert

def run_integration_test():
    print("🚀 STARTING FULL SYSTEM INTEGRITY & SECURITY TEST")
    print("="*50)

    # 1. SETUP
    filename = "top_secret.txt"
    original_content = "This is a secret message from 2026."
    user_pass = "QuantumSafe2026!"
    
    with open(filename, "w") as f:
        f.write(original_content)
    print(f"[*] Created original file: {filename}")

    # --- ENCRYPTION PHASE (PROTECTING) ---
    print("\n[PHASE 1: SECURING FILE]")
    
    # A - Availability: Create safety backup
    availability.create_backup(filename)
    
    # I - Integrity: Fingerprint the healthy file
    orig_hash = integrity.generate_hash(filename)['hash']
    
    # C - Confidentiality: Derive Key & Encrypt
    salt = password.generate_salt()
    salt_str = password.salt_to_str(salt)
    key = password.derive_key(user_pass, salt)
    
    enc_res = encryptor.encrypt_file(filename, key)
    print(f"[+] {enc_res['message']}")

    # S - Storage: Save metadata for later
    storage.store_file_metadata(filename, salt_str, orig_hash)
    print("[+] Security metadata stored in database.")

    # --- ATTACK SIMULATION ---
    print("\n[PHASE 2: ATTACK SIMULATION]")
    # Try to decrypt with WRONG password
    wrong_key = password.derive_key("WrongPassword123", salt)
    dec_fail = encryptor.decrypt_file(enc_res['enc_path'], wrong_key)
    print(f"[*] Attempting decryption with wrong password... Result: {dec_fail['message']}")

    # --- DECRYPTION PHASE (RECOVERING) ---
    print("\n[PHASE 3: AUTHORIZED ACCESS]")
    
    # Retrieve metadata from storage
    meta = storage.get_file_metadata(filename)
    stored_salt = password.str_to_salt(meta['salt'])
    stored_hash = meta['hash']

    # Re-derive correct key
    correct_key = password.derive_key(user_pass, stored_salt)

    # Decrypt
    dec_success = encryptor.decrypt_file(enc_res['enc_path'], correct_key)
    print(f"[+] {dec_success['message']}")

    # Final Integrity Check
    is_valid, status_msg = integrity.verify_file(filename, stored_hash)
    print(f"[*] Final {status_msg}")

    if is_valid:
        print("\n✅ TEST SUCCESS: Data is intact, secure, and recoverable.")
    else:
        print("\n❌ TEST FAILED: Integrity compromised.")

if __name__ == "__main__":
    run_integration_test()