# frontend/main_page.py
from nicegui import ui
from config import config_manager, paths
from services import file_processing, file_matching
import pandas as pd
from datetime import datetime

_matched_df = {
    'df': None,
}


def main_page() -> None:
    ui.label('Process Orders').classes('text-h4')

    config = config_manager.load_config()

    ui.label('Selected Files').classes('text-h5')

    new_items_file = config.get('newitems_file')
    if new_items_file:
        ui.label(f'New Items File: {new_items_file}')
    else:
        ui.label('No New Items File selected.')

    po_files = config.get('po_files', [])
    if po_files:
        ui.label('PO Files:')
        for po in po_files:
            ui.label(f'- {po}')
    else:
        ui.label('No PO Files selected.')

    def start_matching() -> None:
        matched_list = []
        for po_filename in po_files:
            po_path = paths.UPLOADED_PO_DIR / po_filename
            new_items_path = paths.NEW_ITEMS_DIR / new_items_file
            matched_items = file_matching.match_items(po_path, new_items_path, config['po_qty_column'])
            output_filename = f"matched_{po_filename.replace('.xlsx', '')}.csv"
            file_processing.save_matched_items(matched_items, output_filename)
            ui.notify(f'Matched items saved to Newfiletemp/{output_filename}')
            matched_list.append(matched_items)

        if matched_list:
            _matched_df['df'] = pd.concat(matched_list, ignore_index=True)
        else:
            _matched_df['df'] = pd.DataFrame()
        refresh_table()

    ui.button('Start Matching', on_click=start_matching)

    table = ui.table(columns=[], rows=[], row_key='index', selection='multiple')

    def refresh_table() -> None:
        df = _matched_df.get('df')
        if isinstance(df, pd.DataFrame) and not df.empty:
            table.columns = [{'name': c, 'label': c, 'field': c} for c in df.columns]
            table.rows = df.to_dict('records')
            table.update()
    refresh_table()

    def create_new_file() -> None:
        if not table.selected:
            ui.notify('No items selected.', color='warning')
            return
        export_df = pd.DataFrame(table.selected)
        output_path = file_processing.save_selected_items(export_df)
        ui.notify(f'Selected items saved to Newfiletemp/{output_path.name}')

    ui.button('Create new file', on_click=create_new_file)
