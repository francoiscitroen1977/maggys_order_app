# frontend/process_configured_matches.py
"""Page to process matches based on the saved configuration."""

import streamlit as st
from . import main_page


def process_configured_matches_page():
    """Run the matching process using the saved configuration."""
    st.header("Process Configured Matches")
    st.write(
        "Use this page after configuring matching to generate files from the configured settings."
    )
    main_page.main_page()
