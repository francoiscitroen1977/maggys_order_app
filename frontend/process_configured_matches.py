# frontend/process_configured_matches.py
"""Page to review and edit preprocessed item files."""

import streamlit as st
from services import file_processing, utils
from config import paths


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

    # Load dropdown options from JSON files
    categ_codes = utils.load_json_codes(paths.JSON_FILES_DIR / "categories_clean.json", "CATEG_COD")
    subcat_codes = utils.load_json_codes(paths.JSON_FILES_DIR / "subcategories_clean.json", "SUBCAT_COD")
    acct_codes = utils.load_json_codes(paths.JSON_FILES_DIR / "New_Acct_cod.json", "ACCT_COD")

    column_config = {
        "CATEG_COD": st.column_config.SelectboxColumn(
            label="Category Code",
            help="Choose a category code",
            options=categ_codes,
            required=False,
        ),
        "SUBCAT_COD": st.column_config.SelectboxColumn(
            label="Subcategory Code",
            help="Choose a subcategory code",
            options=subcat_codes,
            required=False,
        ),
        "ACCT_COD": st.column_config.SelectboxColumn(
            label="Account Code",
            help="Choose an account code",
            options=acct_codes,
            required=False,
        ),
    }

    editor_key = f"editor_{selected_file}"
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        column_config=column_config,
        use_container_width=True,
        key=editor_key,
    )

    if edited_df is not None:
        st.session_state[f"edited_{selected_file}"] = edited_df

    csv_df = st.session_state.get(f"edited_{selected_file}", df)
    csv_data = csv_df.to_csv(index=False).encode("utf-8")

    st.caption("⚠️ Please press Enter or click outside the cell after editing before downloading.")
    st.download_button(
        "Download CSV",
        data=csv_data,
        file_name=f"updated_{selected_file}",
        mime="text/csv",
    )
