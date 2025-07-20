# services/utils.py
from pathlib import Path
import json
from typing import List

def clean_filename(filename: str) -> str:
    return filename.replace(" ", "_").replace("(", "").replace(")", "")

def ensure_directories_exist(paths_list):
    for path in paths_list:
        Path(path).mkdir(parents=True, exist_ok=True)


def load_json_codes(json_path: Path, code_key: str) -> List[str]:
    """Return a list of codes from a JSON file."""
    if not json_path.exists():
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = [data]
    return [str(item.get(code_key, "")) for item in data if code_key in item]
