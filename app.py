# app.py
import streamlit as st
from frontend import (
    config_page,
    main_page,
    configure_matching,
    process_configured_matches,
)

# Expand the page layout so wide tables utilize more horizontal space
st.set_page_config(page_title="Maggys Order App", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Configure matching",
        "Pre-process matching",
        "Process configured matches",
    ],
    key="current_page",
)

if page == "Pre-process matching":
    main_page.main_page()
elif page == "Configure matching":
    configure_matching.configure_matching_page()
else:
    process_configured_matches.process_configured_matches_page()
