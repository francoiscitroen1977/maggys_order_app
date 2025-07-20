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

    # ✅ Ensure all editable columns are string type to avoid Selectbox casting errors
    for col in ["ITEM_NO", "DESCR", "ITEM_VEND_NO", "CATEG_COD", "SUBCAT_COD", "ACCT_COD"]:
        if col in df.columns:
            df[col] = df[col].astype(str).fillna("")

    # ✅ Load dropdown options and ensure they're strings too
    categ_codes = [str(c) for c in utils.load_json_codes(paths.JSON_FILES_DIR / "categories_clean.json", "CATEG_COD")]
    subcat_codes = [str(s) for s in utils.load_json_codes(paths.JSON_FILES_DIR / "subcategories_clean.json", "SUBCAT_COD")]
    acct_codes = [str(a) for a in utils.load_json_codes(paths.JSON_FILES_DIR / "New_Acct_cod.json", "ACCT_COD")]

    column_config = {
        "ITEM_NO": st.column_config.TextColumn("Item Number"),
        "DESCR": st.column_config.TextColumn("Description"),
        "ITEM_VEND_NO": st.column_config.TextColumn("Vendor Code"),

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
    session_key = f"edited_{selected_file}"

    # Display editable table
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        column_config=column_config,
        use_container_width=True,
        key=editor_key,
    )

    # Save button to commit edits to session state
    if st.button("Save Changes"):
        st.session_state[session_key] = edited_df
        st.success("Changes saved. You can now download the updated file.")

    # Use updated version from session or original
    csv_df = st.session_state.get(session_key)

    # Show download button only if saved
    if csv_df is not None:
        csv_data = csv_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv_data,
            file_name=f"updated_{selected_file}",
            mime="text/csv",
        )
    else:
        st.caption("⚠️ Edit values and click 'Save Changes' before downloading.")
