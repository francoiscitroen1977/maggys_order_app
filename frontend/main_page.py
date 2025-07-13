# frontend/main_page.py
import streamlit as st
from config import config_manager, paths
from services import file_processing, file_matching

def main_page():
    st.header("Process Orders")

    config = config_manager.load_config()

    for po_filename in config["po_files"]:
        po_path = paths.UPLOADED_PO_DIR / po_filename
        new_items_path = paths.NEW_ITEMS_DIR / config["newitems_file"]
        matched_items = file_matching.match_items(po_path, new_items_path, config["po_qty_column"])
        output_filename = f"matched_{po_filename.replace('.xlsx', '')}.csv"
        file_processing.save_matched_items(matched_items, output_filename)
        st.success(f"Matched items saved to {output_filename}")
