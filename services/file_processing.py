# services/file_processing.py
import pandas as pd
from config import paths
from datetime import datetime
from services import logger

def list_files_in_directory(directory_path):
    return [f.name for f in directory_path.glob("*.*") if f.is_file()]

def list_preprocessed_files():
    """Return all files starting with ``preprocessed_`` in the temp directory."""
    paths.NEW_ITEMS_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    return [f.name for f in paths.NEW_ITEMS_TEMP_DIR.glob("preprocessed_*") if f.is_file()]

def read_full_price_file(filename):
    file_path = paths.FULL_PRICE_DIR / filename
    return pd.read_excel(file_path)

def read_new_items_file(filename):
    file_path = paths.NEW_ITEMS_DIR / filename
    df = pd.read_csv(file_path)
    logger.log(f"Read new items file {filename}", df)
    return df

def read_po_file(filename):
    file_path = paths.UPLOADED_PO_DIR / filename
    df = pd.read_excel(file_path)
    logger.log(f"Read PO file {filename}", df)
    return df


def save_matched_items(df, output_filename):
    """Save matched items to the temporary New Items directory."""
    paths.NEW_ITEMS_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    output_path = paths.NEW_ITEMS_TEMP_DIR / output_filename
    df.to_csv(output_path, index=False)
    logger.log(f"Saved matched items to {output_filename}", df)
    return output_path


def save_selected_items(df, source_filename: str):
    """Save selected rows using the original filename with ``preprocessed_`` prefix."""
    paths.NEW_ITEMS_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"preprocessed_{source_filename}"
    output_path = paths.NEW_ITEMS_TEMP_DIR / filename
    df.to_csv(output_path, index=False)
    logger.log(f"Saved selected items to {filename}", df)
    return output_path


def read_preprocessed_file(filename):
    """Read a preprocessed file from the temporary directory."""
    file_path = paths.NEW_ITEMS_TEMP_DIR / filename
    df = pd.read_csv(file_path)
    logger.log(f"Read preprocessed file {filename}", df)
    return df


def save_preprocessed_file(df, filename):
    """Overwrite an existing preprocessed file in the temporary directory."""
    paths.NEW_ITEMS_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    file_path = paths.NEW_ITEMS_TEMP_DIR / filename
    df.to_csv(file_path, index=False)
    logger.log(f"Saved edited preprocessed file {filename}", df)
    return file_path


def copy_to_processed_new(filename):
    """Copy a file from the temp directory to the ProcessedNew directory."""
    paths.PROCESSED_NEW_DIR.mkdir(parents=True, exist_ok=True)
    src = paths.NEW_ITEMS_TEMP_DIR / filename
    dest = paths.PROCESSED_NEW_DIR / filename
    if src.exists():
        dest.write_bytes(src.read_bytes())
        logger.log(f"Copied {filename} to ProcessedNew")
    return dest
