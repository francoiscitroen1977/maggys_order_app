# frontend/main_page.py
import streamlit as st
from config import config_manager
from services import file_processing, file_matching

def main_page():
    st.header("Process Orders")

    config = config_manager.load_config()

    full_price_df = file_processing.read_full_price_file(config["full_price_file"])
    new_items_df = file_processing.read_new_items_file(config["newitems_file"])

    for po_filename in config["po_files"]:
        po_df = file_processing.read_po_file(po_filename)
        matched_items = file_matching.match_items(po_df, new_items_df, config["po_qty_column"])
        output_filename = f"matched_{po_filename.replace('.xlsx', '')}.csv"
        file_processing.save_matched_items(matched_items, output_filename)
        st.success(f"Matched items saved to {output_filename}")