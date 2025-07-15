# config/config_manager.py
import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        # Remove legacy key if present
        config.pop("full_price_file", None)
        return config
    return {
        "newitems_file": None,
        "po_files": [],
        "po_qty_column": "Sales Products Qty",
    }


def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)


def update_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)