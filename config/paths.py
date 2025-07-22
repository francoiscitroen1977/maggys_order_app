# config/paths.py
from pathlib import Path

# Base directory for external data storage
BASE_DIR = Path(r"C:/Users/Public/ItemImport")

# Directory containing the dropdown option JSON files
# These JSON files live inside the same BASE_DIR used for other inputs.
JSON_FILES_DIR = BASE_DIR / "JsonFiles"

FULL_PRICE_DIR = BASE_DIR / "Docs"
NEW_ITEMS_DIR = BASE_DIR / "New"
NEW_ITEMS_TEMP_DIR = BASE_DIR / "Newfiletemp"
UPLOADED_PO_DIR = BASE_DIR / "UploadedPO"
LOG_DIR = BASE_DIR / "log"
PROCESSED_NEW_DIR = BASE_DIR / "ProcessedNew"
