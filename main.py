import sys
from getpass import getpass
from core import config, alert, availability, integrity, password, encryptor, storage

def display_banner():
    print("\n" + "="*50)
    print("      🛡️  SECUREFILEGUARD v1.0 - CIA TRIAD 🛡️")
    print("="*50)

def main_menu():
    display_banner()
    
    # SECURITY CHECK 1: Database Integrity
    if not storage.verify_storage_integrity():
        print("🚨 CRITICAL: Database tampering detected! System locked.")
        alert.log_event("critical", "System startup blocked due to database signature mismatch.")
        sys.exit(1)

    while True:
        print("\n[MAIN MENU]")
        print("1. 🔒 Secure File (Encrypt + Backup)")
        print("2. 🔓 Unlock File (Decrypt + Verify)")
        print("3. 🔄 Restore from Backup")
        print("4. 📋 View Security Logs")
        print("5. 🚪 Exit")
        
        choice = input("\nSelect an option: ")

        if choice == '1':
            handle_encryption()
        elif choice == '2':
            handle_decryption()
        elif choice == '3':
            handle_restore()
        elif choice == '4':
            view_logs()
        elif choice == '5':
            print("👋 Exiting SecureFileGuard. Stay safe!")
            break
        else:
            print("❌ Invalid selection. Please try again.")

def handle_encryption():
    file_path = input("Enter filename to secure: ")
    user_pass = getpass("Set an encryption password: ")
    
    # 1. Availability: Create Backup
    print("[*] Creating safety backup...")
    availability.create_backup(file_path)

    # 2. Integrity: Generate original fingerprint
    print("[*] Generating integrity hash...")
    orig_hash = integrity.generate_hash(file_path)['hash']

    # 3. Confidentiality: Key Derivation & Encryption
    print("[*] Deriving secure key and encrypting...")
    salt = password.generate_salt()
    key = password.derive_key(user_pass, salt)
    
    res = encryptor.encrypt_file(file_path, key)
    
    if res['status'] == 'success':
        # 4. Storage: Save Metadata
        salt_str = password.salt_to_str(salt)
        storage.store_file_metadata(file_path, salt_str, orig_hash)
        print(f"✅ SUCCESS: {res['message']}")
    else:
        print(f"❌ ERROR: {res['message']}")

def handle_restore():
    file_path = input("Enter filename to restore: ")
    
    # Check for available versions
    versions = availability.list_versions(file_path)
    if not versions:
        print("❌ No backups found for this file.")
        return

    print("\nAvailable versions (Latest first):")
    for i, v in enumerate(versions, 1):
        print(f"{i}. {v}")
    
    res = availability.restore_backup(file_path)
    print(f"[*] {res['message']}")

def handle_decryption():
    file_path = input("Enter filename to unlock (include .enc): ")
    user_pass = getpass("Enter decryption password: ")

    # 1. Storage: Get Metadata
    meta = storage.get_file_metadata(file_path.replace(".enc", ""))
    if not meta:
        print("❌ Error: No security metadata found for this file.")
        return

    # 2. Password: Re-derive Key
    salt = password.str_to_salt(meta['salt'])
    key = password.derive_key(user_pass, salt)

    # 3. Confidentiality: Decrypt
    print("[*] Unlocking file...")
    res = encryptor.decrypt_file(file_path, key)

    if res['status'] == 'success':
        # 4. Integrity: Verify if data is still clean
        print("[*] Verifying file integrity...")
        original_name = res['original_path']
        is_valid, msg = integrity.verify_file(original_name, meta['hash'])
        
        if is_valid:
            print(f"✅ SUCCESS: {msg}")
        else:
            print(f"⚠️ WARNING: {msg}")
            choice = input("Would you like to restore the latest clean backup? (y/n): ")
            if choice.lower() == 'y':
                availability.restore_backup(original_name)
    else:
        print(f"❌ ERROR: {res['message']}")

def view_logs():
    print("\n--- RECENT SECURITY EVENTS ---")
    if config.LOG_FILE.exists():
        with open(config.LOG_FILE, "r") as f:
            # Show last 10 log entries
            lines = f.readlines()
            for line in lines[-10:]:
                print(line.strip())
    else:
        print("No logs found.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted. Closing securely.")
        sys.exit(0)