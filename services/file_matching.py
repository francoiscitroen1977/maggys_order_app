# services/file_matching.py
import pandas as pd
from services import logger


def match_items(po_file, new_items_file, po_qty_column="Sales Products Qty", upc_column="UPC Code"):
    po_df = pd.read_excel(po_file, sheet_name="Final Customer Price List", skiprows=8)
    new_items_df = pd.read_csv(new_items_file)
    logger.log(f"Matching items using {po_file} and {new_items_file}")

    po_df_filtered = po_df[(po_df[po_qty_column] > 1) & (po_df[upc_column].notnull())]
    po_upc_codes = po_df_filtered[upc_column].astype(str).unique()
    matched_items = new_items_df[new_items_df['BARCOD'].astype(str).isin(po_upc_codes)]

    logger.log("Matched items", matched_items)
    return matched_items
