from pathlib import Path

# --- CRYPTOGRAPHY SETTINGS ---
KDF_ITERATIONS = 480000 
KEY_LENGTH = 32
SALT_SIZE = 16

# --- DIRECTORY SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = BASE_DIR / ".backups"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# --- FILE SETTINGS ---
DB_FILE = DATA_DIR / "file_db.json"
SIG_FILE = DATA_DIR / ".db.sig"
LOG_FILE = LOG_DIR / "security.log"

# --- I/O SETTINGS ---
BUFFER_SIZE = 131072  # 128KB