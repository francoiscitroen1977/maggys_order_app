# services/utils.py
from pathlib import Path

def clean_filename(filename: str) -> str:
    return filename.replace(" ", "_").replace("(", "").replace(")", "")

def ensure_directories_exist(paths_list):
    for path in paths_list:
        Path(path).mkdir(parents=True, exist_ok=True)
