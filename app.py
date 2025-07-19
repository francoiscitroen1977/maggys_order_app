# app.py
import streamlit as st
from frontend import (
    config_page,
    main_page,
    configure_matching,
    process_configured_matches,
)

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Pre-process matching",
        "Configure matching",
        "Process configured matches",
    ],
)

if page == "Pre-process matching":
    main_page.main_page()
elif page == "Configure matching":
    configure_matching.configure_matching_page()
else:
    process_configured_matches.process_configured_matches_page()