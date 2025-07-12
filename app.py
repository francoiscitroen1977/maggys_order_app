# app.py
import streamlit as st
from frontend import config_page, main_page

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Configuration", "Main Page"])

if page == "Configuration":
    config_page.config_page()
else:
    main_page.main_page()