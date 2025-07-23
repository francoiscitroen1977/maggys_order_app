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
        st.info("No preprocessed files found in Newfiletemp.")
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

        # Write the edited data back to the temp directory
        updated_filename = f"updated_{selected_file}"
        file_processing.save_preprocessed_file(edited_df, updated_filename)

        # Create the additional price file based on the edited data
        required_cols = {"ITEM_NO", "PRC_1", "PRC_2"}
        if required_cols.issubset(edited_df.columns):
            price_df = edited_df[["ITEM_NO", "PRC_1", "PRC_2"]].copy()
            price_df.insert(1, "LOC_ID", "*")
            price_df.insert(2, "DIM_1_UPR", "*")
            price_df.insert(3, "DIM_2_UPR", "*")
            price_df.insert(4, "DIM_3_UPR", "*")
            price_df = price_df[
                [
                    "ITEM_NO",
                    "LOC_ID",
                    "DIM_1_UPR",
                    "DIM_2_UPR",
                    "DIM_3_UPR",
                    "PRC_1",
                    "PRC_2",
                ]
            ]
            price_filename = f"price_{updated_filename}"
            file_processing.save_preprocessed_file(price_df, price_filename)


        st.success("Changes saved. You can now save the new files.")


    # Use updated version from session or original
    csv_df = st.session_state.get(session_key)

    # Allow saving edited files to the ProcessedNew directory
    if csv_df is not None:
        if st.button("Save new Files"):
            updated_filename = f"updated_{selected_file}"
            price_filename = f"price_{updated_filename}"
            file_processing.copy_to_processed_new(updated_filename)
            file_processing.copy_to_processed_new(price_filename)
            st.success("Files saved to ProcessedNew.")
    else:
        st.caption("⚠️ Edit values and click 'Save Changes' before saving files.")
