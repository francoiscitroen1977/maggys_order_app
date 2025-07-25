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

# Initialize session state for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Configure matching"

# Redirect to a different page if requested
if "redirect_to_page" in st.session_state:
    st.session_state.current_page = st.session_state.redirect_to_page
    del st.session_state.redirect_to_page

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
