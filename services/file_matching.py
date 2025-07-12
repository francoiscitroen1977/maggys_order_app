# services/file_matching.py
import pandas as pd


def match_items(po_df, new_items_df, po_qty_column, upc_column="UPC Code"):
    # Filter PO items where Qty > 0
    po_df_filtered = po_df[po_df[po_qty_column] > 0]

    # Ensure UPC columns are strings to avoid NaN float issues
    po_upc_codes = po_df_filtered[upc_column].astype(str).unique()

    # Filter new items where BARCOD matches one of the PO UPCs
    matched_items = new_items_df[new_items_df['BARCOD'].astype(str).isin(po_upc_codes)]
    return matched_items