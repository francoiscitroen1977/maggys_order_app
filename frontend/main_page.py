# frontend/main_page.py
import streamlit as st
from config import config_manager, paths
from services import file_processing, file_matching
import pandas as pd
from datetime import datetime

def main_page():
    st.header("Process Orders")

    config = config_manager.load_config()

    st.subheader("Selected Files")

    new_items_file = config.get("newitems_file")
    if new_items_file:
        st.write(f"New Items File: {new_items_file}")
    else:
        st.write("No New Items File selected.")

    po_files = config.get("po_files", [])
    if po_files:
        st.write("PO Files:")
        for po in po_files:
            st.write(f"- {po}")
    else:
        st.write("No PO Files selected.")

    if st.button("Start Matching"):
        matched_list = []
        for po_filename in po_files:
            po_path = paths.UPLOADED_PO_DIR / po_filename
            new_items_path = paths.NEW_ITEMS_DIR / new_items_file
            matched_items = file_matching.match_items(po_path, new_items_path, config["po_qty_column"])
            output_filename = f"matched_{po_filename.replace('.xlsx', '')}.csv"
            file_processing.save_matched_items(matched_items, output_filename)
            st.success(f"Matched items saved to {output_filename}")
            matched_list.append(matched_items)

        if matched_list:
            st.session_state["matched_df"] = pd.concat(matched_list, ignore_index=True)
        else:
            st.session_state["matched_df"] = pd.DataFrame()

    matched_df = st.session_state.get("matched_df")
    if isinstance(matched_df, pd.DataFrame) and not matched_df.empty:
        st.subheader("Matched Items")
        selected_indices = []
        for idx, row in matched_df.iterrows():
            label_parts = [str(row[col]) for col in matched_df.columns[:2]]
            if st.checkbox(" - ".join(label_parts), key=f"sel_{idx}"):
                selected_indices.append(idx)

        if st.button("Create new file"):
            if selected_indices:
                export_df = matched_df.loc[selected_indices]
                output_path = file_processing.save_selected_items(export_df)
                st.success(f"Selected items saved to {output_path.name}")
            else:
                st.warning("No items selected.")
