# services/file_processing.py
import pandas as pd
from config import paths

def list_files_in_directory(directory_path):
    return [f.name for f in directory_path.glob("*.*") if f.is_file()]

def read_full_price_file(filename):
    file_path = paths.FULL_PRICE_DIR / filename
    return pd.read_excel(file_path)

def read_new_items_file(filename):
    file_path = paths.NEW_ITEMS_DIR / filename
    return pd.read_csv(file_path)

def read_po_file(filename):
    file_path = paths.UPLOADED_PO_DIR / filename
    return pd.read_excel(file_path)


def save_matched_items(df, output_filename):
    output_path = paths.NEW_ITEMS_DIR / output_filename
    df.to_csv(output_path, index=False)
    return output_path
