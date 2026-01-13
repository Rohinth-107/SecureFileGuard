import logging
from pathlib import Path
from datetime import datetime

# Setup
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "security.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_event(level: str, message: str):
    """Logs security events to the log file and provides console feedback."""
    level = level.lower()
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    elif level == "critical":
        logging.critical(message)
    
    # Optional: Visual feedback for the CLI
    # print(f"[*] {message}") 

# NEW: Add a session separator to the log file on import
logging.info("="*50)
logging.info(f"NEW SESSION STARTED AT {datetime.now()}")
logging.info("="*50)