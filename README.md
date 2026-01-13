🛡️ SecureFileGuard v1.0
SecureFileGuard is a professional-grade Python security suite designed to protect sensitive data using the CIA Triad (Confidentiality, Integrity, and Availability). It combines high-entropy key derivation, AES-256 encryption, SHA-256 fingerprinting, and versioned backups into a single command-line interface.

🚀 Key Features
1. Confidentiality (The Lock)
AES-256 Encryption: Utilizes Fernet (symmetric encryption) which ensures that data cannot be read without the correct key.

PBKDF2 Key Derivation: Human passwords are "stretched" using 480,000 iterations of SHA-256 with a unique 16-byte salt to thwart brute-force and rainbow table attacks.

Memory Safety: Uses getpass for secure password entry, preventing shoulder-surfing.

2. Integrity (The Fingerprint)
SHA-256 File Hashing: Generates a unique digital fingerprint for every file. Any unauthorized modification—even a single bit—is detected during decryption.

Database Signature: The internal metadata store (file_db.json) is protected by a Master Signature. If the database itself is tampered with, the system locks down to prevent spoofing attacks.

3. Availability (The Safety Net)
Timestamped Versioning: Automatically creates backups with a YYYYMMDD_HHMMSS format, allowing for point-in-time recovery.

Automated Recovery: If an integrity breach is detected during decryption, the system offers an immediate "one-click" restoration from the latest healthy backup.

🏗️ Architecture & Project Structure
The project follows a modular "Core-Engine" pattern for high maintainability and zero hard-coding:

Plaintext

SecureFileGuard/
├── core/
│   ├── config.py       # Centralized security & path settings
│   ├── alert.py        # Audit trail & logging engine
│   ├── availability.py # Versioned backup & restore logic
│   ├── integrity.py    # SHA-256 hashing & verification
│   ├── password.py     # PBKDF2 key derivation logic
│   ├── encryptor.py    # Fernet (AES) encryption engine
│   └── storage.py      # Metadata management & DB signature
├── data/               # Secure metadata storage (JSON)
├── logs/               # Security audit logs
├── .backups/           # Hidden versioned backups
├── main.py             # Integrated CLI Control Center
└── tests.py            # End-to-end system integration tests
🛠️ Technical Standards
Python 3.10+

Cryptography: cryptography library (Standard for production security).

Path Management: pathlib for cross-platform (Windows/Linux) compatibility.

Logging: Native logging library for persistent security auditing.

🚦 Getting Started
Prerequisites
Bash

pip install cryptography
Usage
Clone the repository.

Run the tool:

Bash

python main.py
Follow the On-Screen Dashboard:

Select Option 1 to encrypt and backup a file.

Select Option 2 to decrypt and verify integrity.

Use the Log Viewer (Option 4) to inspect the audit trail.

🛡️ Security Audit Log
Every security-sensitive event is recorded in logs/security.log.

[INFO]: Successful encryption/decryption.

[WARNING]: Failed password attempts.

[CRITICAL]: Integrity breaches or database tampering detections.

👨‍💻 Developer Note
This project was built to demonstrate a deep understanding of cryptographic workflows and security best practices. It avoids common pitfalls by using non-hardcoded configurations, atomic file operations, and comprehensive error handling.