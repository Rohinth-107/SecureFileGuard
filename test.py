# main.py
from core.availability import create_backup,restore_backup
from core.integrity import verify_file,generate_hash
from core.password import generate_salt, derive_key
from core.encryptor import encrypt_file, decrypt_file

def test_confidential():
    # 1. Setup
    file_to_lock = "secret.txt"
    with open(file_to_lock, "w") as f: f.write("Top Secret Content")
    password = "my_password_123"

    # 2. Key Process
    salt = generate_salt()
    key = derive_key(password, salt)

    # 3. Encrypt
    print("Encrypting...")
    res = encrypt_file(file_to_lock, key)
    print(res['message'])

    # 4. Decrypt
    print("\nDecrypting...")
    res_dec = decrypt_file(res['enc_path'], key)
    print(res_dec['message'])

def test_availability():
    test_file = "secure_test.txt"
    with open(test_file, "w") as f:
        f.write("Important backup data.")

    # 1. Test Backup
    print("--- Testing Backup ---")
    res_b = create_backup(test_file)
    print(f"Status: {res_b['status'].upper()} | {res_b['message']}")

    # 2. Test Restore
    print("\n--- Testing Restore ---")
    res_r = restore_backup(test_file)
    print(f"Status: {res_r['status'].upper()} | {res_r['message']}")

def test_integrity():
    # Test with a full path if you want!
    test_file = "integrity_demo.txt"

    with open(test_file, "w") as f:
        f.write("Cybersecurity is about layers.")

    # Generate Hash
    result = generate_hash(test_file)
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
        print(f"🔑 Hash: {result['hash']}")

    with open(test_file, "w") as f:
        f.write("Cybersecurity is about Layers.")   #file is modified

    # Verify
    is_valid, msg = verify_file(test_file, result['hash'])
    print(f"🧐 Status: {msg}")
    # If is_valid is True, it means NOT modified. 
    # If is_valid is False, it means IT IS modified.
    print(f"Is the file authentic (unmodified)? : {is_valid}")






if __name__ == "__main__":
    #test_availability()
    #test_integrity()
    test_confidential()
