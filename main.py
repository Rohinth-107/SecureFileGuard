# main.py
from core import integrity, encryptor, availability
from core.availability import create_backup,restore_backup
import os

def run_test():
    filename = "sample_data.txt"  #can also use the file path
    
    # 1. Setup: Create a real file
    with open(filename, "w") as f:
        f.write("This is highly sensitive information.")
    print(f"--- Created {filename} ---")

    # 2. Test Backup
    print("\nStep 1: Testing Backup...")
    result = create_backup(filename)
    if result and os.path.exists("backups/sample_data.txt.bak"):
        print("✅ Backup file verified in backups/ folder.")

    # 3. Test Corruption: Modify the original file
    print("\nStep 2: Simulating File Corruption...")
    with open(filename, "w") as f:
        f.write("I AM CORRUPTED BY A HACKER!!!")
    
    with open(filename, "r") as f:
        print(f"Current File Content: {f.read()}")

    # 4. Test Restore
    print("\nStep 3: Testing Restore...")
    if restore_backup(filename):
        with open(filename, "r") as f:
            content = f.read()
            print(f"Restored File Content: {content}")
            if content == "This is highly sensitive information.":
                print("✅ Restore verified: Content is correct!")

    # 5. Cleanup (Optional)
    # os.remove(filename)

if __name__ == "__main__":
    run_test()

def main():
    print("--- SecureFileGuard CLI Initialized ---")
    # This is where your menu loop will go later
    print("System Ready.")
