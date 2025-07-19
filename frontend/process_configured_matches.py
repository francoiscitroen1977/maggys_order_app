# frontend/process_configured_matches.py
"""Page to review and edit preprocessed item files."""

import streamlit as st
from services import file_processing


def process_configured_matches_page():
    """Display an editable view of a preprocessed file."""
    st.header("Process Configured Matches")

    preprocessed_files = file_processing.list_preprocessed_files()
    if not preprocessed_files:
        st.info("No PreProcess_NewItems files found in Newfiletemp.")
        return

    selected_file = st.selectbox("Select Preprocessed File", preprocessed_files)
    if not selected_file:
        return

    df = file_processing.read_preprocessed_file(selected_file)
    edited_df = st.data_editor(df, num_rows="dynamic")

    if st.button("Save Changes"):
        file_processing.save_preprocessed_file(edited_df, selected_file)
        st.success(f"Saved changes to {selected_file}")
