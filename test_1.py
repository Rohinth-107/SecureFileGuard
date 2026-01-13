import os
from pathlib import Path
from core import availability, integrity, password, encryptor, storage

class SecureFileGuardTester:
    def __init__(self):
        self.test_file = "test_data.txt"
        self.test_pass = "ComplexPass123!"
        self._setup_test_file()

    def _setup_test_file(self):
        """Creates a fresh test file before each run."""
        with open(self.test_file, "w") as f:
            f.write("This is a test of the SecureFileGuard system.")

    def test_availability_module(self):
        print("\n--- [A] TESTING AVAILABILITY ---")
        # Test Backup
        res_b = availability.create_backup(self.test_file)
        print(f"Backup: {res_b['message']}")
        
        # Test Corruption & Restore
        with open(self.test_file, "a") as f: f.write("CORRUPTION")
        res_r = availability.restore_backup(self.test_file)
        print(f"Restore: {res_r['message']}")
        
        return res_r['status'] == 'success'

    def test_integrity_module(self):
        print("\n--- [I] TESTING INTEGRITY ---")
        # Generate initial hash
        res_h = integrity.generate_hash(self.test_file)
        original_hash = res_h['hash']
        print(f"Hash Generated: {original_hash[:16]}...")

        # Verify clean file
        valid, msg = integrity.verify_file(self.test_file, original_hash)
        print(f"Clean Check: {msg}")

        # Verify tampered file
        with open(self.test_file, "a") as f: f.write("!")
        valid_tamper, msg_tamper = integrity.verify_file(self.test_file, original_hash)
        print(f"Tamper Check: {msg_tamper}")
        
        return valid == True and valid_tamper == False

    def test_confidentiality_module(self):
        print("\n--- [C] TESTING CONFIDENTIALITY ---")
        # Key Derivation
        salt = password.generate_salt()
        key = password.derive_key(self.test_pass, salt)
        print("Key derived successfully.")

        # Encryption
        res_e = encryptor.encrypt_file(self.test_file, key)
        print(f"Encryption: {res_e['message']}")

        # Decryption
        res_d = encryptor.decrypt_file(res_e['enc_path'], key)
        print(f"Decryption: {res_d['message']}")

        return res_d['status'] == 'success'

    def test_storage_module(self):
        print("\n--- [S] TESTING STORAGE ---")
        fake_salt = "dGhpcyBpcyBhIHNhbHQ="
        fake_hash = "e6188f7a1671d789a3038d1fa25e9310f"
        
        res = storage.store_file_metadata("dummy.txt", fake_salt, fake_hash)
        print(f"Save: {res['message']}")
        
        data = storage.get_file_metadata("dummy.txt")
        if data and data['hash'] == fake_hash:
            print("Read: Success (Metadata matches)")
            return True
        return False

# --- Execution Block ---
if __name__ == "__main__":
    tester = SecureFileGuardTester()
    
    # Run tests individually
    results = {
        "Availability": tester.test_availability_module(),
        "Integrity": tester.test_integrity_module(),
        "Confidentiality": tester.test_confidentiality_module(),
        "Storage": tester.test_storage_module()
    }

    print("\n" + "="*30)
    print("FINAL TEST REPORT")
    print("="*30)
    for module, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{module:15}: {status}")