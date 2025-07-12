# frontend/upload_page.py
import streamlit as st
from config import paths
import shutil

def upload_page():
    st.header("Upload PO File")
    uploaded_file = st.file_uploader("Choose a PO file", type=["xlsx"])
    if uploaded_file is not None:
        save_path = paths.UPLOADED_PO_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)
        st.success(f"File {uploaded_file.name} uploaded successfully!")