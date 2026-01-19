
# 🛡️ SecureFileGuard v1.0

SecureFileGuard is a **professional-grade Python security suite** designed to protect sensitive data using the **CIA Triad**:

- 🔐 Confidentiality  
- 🧬 Integrity  
- 🧯 Availability  

It combines **high-entropy key derivation**, **AES-256 encryption**, **SHA-256 fingerprinting**, and **versioned backups** into a single **command-line interface (CLI)**.

---

## 🚀 Key Features

### 1️⃣ Confidentiality (The Lock)

- **AES-256 Encryption**  
  Uses **Fernet (symmetric encryption)** to ensure data cannot be read without the correct key.

- **PBKDF2 Key Derivation**  
  Human passwords are strengthened using **480,000 iterations of SHA-256** with a **unique 16-byte salt**, protecting against:
  - Brute-force attacks
  - Rainbow table attacks

- **Memory Safety**  
  Uses `getpass` for secure password entry, preventing shoulder-surfing and password exposure

### 2️⃣ Integrity (The Fingerprint)

- **SHA-256 File Hashing**  
  Generates a unique digital fingerprint for every file.  
  Any unauthorized modification—even **one bit**—is detected during decryption.

- **Database Signature Protection**  
  The internal metadata store (`file_db.json`) is protected by a **Master Signature**.  
  If the database is tampered with, the system **locks down automatically** to prevent spoofing attacks.

### 3️⃣ Availability (The Safety Net)

- **Timestamped Versioning**  
  Automatically creates backups using the format:
  YYYYMMDD_HHMMSS
  This allows **point-in-time recovery**.

- **Automated Recovery**  
If an integrity breach is detected during decryption, SecureFileGuard offers a **one-click restoration** from the most recent healthy backup.

---

## 🏗️ Architecture Overview

SecureFileGuard is built using a **modular Core-Engine pattern**, where each security responsibility is isolated into its own engine.  

This design provides:
- ✅ Clear separation of concerns  
- ✅ Easy testing and debugging  
- ✅ Future extensibility (new engines can be plugged in)  
- ✅ Strong security boundaries between components  

The `main.py` file acts as an **orchestrator**, coordinating all engines through a unified CLI interface.

---

## 📂 Project Structure

```text
SecureFileGuard/
├── core/
│   ├── config.py        # Centralized security & path settings
│   ├── alert.py         # Audit trail & logging engine
│   ├── availability.py # Versioned backup & restore logic
│   ├── integrity.py    # SHA-256 hashing & verification
│   ├── password.py     # PBKDF2 key derivation logic
│   ├── encryptor.py    # Fernet (AES) encryption engine
│   └── storage.py      # Metadata management & DB signature
│
├── data/                # Secure metadata storage (JSON)
├── logs/                # Security audit logs
├── .backups/            # Hidden versioned backups
│
├── main.py              # Integrated CLI Control Center
└── tests.py             # End-to-end system integration tests
```
---

## 🛠️ Technical Standards

- **Python**: 3.10+
- **Cryptography**: `cryptography` library (industry standard for production-grade security)
- **Path Management**: `pathlib` for cross-platform compatibility (Windows/Linux/macOS)
- **Logging**: Python’s native `logging` module for persistent security auditing

---

## ⚙️ Setup Procedure

Follow the steps below to set up **SecureFileGuard** on your local system.

### 1️⃣ Prerequisites

Ensure the following are installed on your system:

- Python 3.10 or higher  
- `pip` (Python package manager)  
- Git (optional, for cloning the repository)

Verify your Python installation:

```bash
python --version
```

### 2️⃣ Clone the Repository 

```bash
git clone https://github.com/your-username/SecureFileGuard.git
cd SecureFileGuard
```
(Skip this step if you downloaded the source code manually.)

### 3️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the virtual environment:
**Windows**
```bash
venv\Scripts\activate
```
**Linux / macOS**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Initialize Required Directories

Ensure the following directories exist (they may be created automatically on first run):
```text  
data/
logs/
.backups/
```

### 6️⃣ Run the Application

```bash
python main.py
```

Follow the CLI prompts to encrypt, verify, or restore files.

**🧪 (Optional) Run Tests**
To verify correct installation:
```bash
python tests.py
```
### ✅ Setup Complete
If the application launches without errors, SecureFileGuard is ready for use.

--- 

### 🧠 Professional Tips
Always run inside a virtual environment
Never commit data/, logs/, or .backups/ to public repositories
Use strong passwords for crptographic operations

---

## 👨‍💻 Developer Note
This project was built to demonstrate a deep understanding of cryptographic workflows and security best practices. It avoids common pitfalls by using non-hardcoded configurations, atomic file operations, and comprehensive error handling.

---
