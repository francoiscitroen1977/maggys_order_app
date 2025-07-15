# frontend/config_page.py
import streamlit as st
from config import config_manager, paths
from services import file_processing
import shutil

def config_page():
    st.header("Configuration")

    config = config_manager.load_config()

    new_items_files = file_processing.list_files_in_directory(paths.NEW_ITEMS_DIR)
    po_files = file_processing.list_files_in_directory(paths.UPLOADED_PO_DIR)

    uploaded_po = st.file_uploader("Upload PO File", type=["xlsx"])
    if uploaded_po is not None:
        save_path = paths.UPLOADED_PO_DIR / uploaded_po.name
        with open(save_path, "wb") as f:
            shutil.copyfileobj(uploaded_po, f)
        st.success(f"File {uploaded_po.name} uploaded successfully!")
        po_files = file_processing.list_files_in_directory(paths.UPLOADED_PO_DIR)

    config["newitems_file"] = st.selectbox("Select New Items File", new_items_files, index=new_items_files.index(config.get("newitems_file")) if config.get("newitems_file") else 0)
    config["po_files"] = st.multiselect("Select PO Files", po_files, default=config.get("po_files", []))

    config["po_qty_column"] = st.text_input("PO Quantity Column Name", config.get("po_qty_column", "Sales Products Qty"))

    if len(po_files) == 0:
        st.warning("No PO files available. Please upload a PO file before saving.")

    save_disabled = len(po_files) == 0 or len(config.get("po_files", [])) == 0

    if st.button("Save Configuration", disabled=save_disabled):
        config_manager.save_config(config)
        st.success("Configuration Saved!")
