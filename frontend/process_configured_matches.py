# frontend/process_configured_matches.py
"""Page to review and edit preprocessed item files."""

from nicegui import ui
from services import file_processing, utils
from config import paths


_edit_store = {}


def process_configured_matches_page() -> None:
    """Display an editable view of a preprocessed file."""
    ui.label('Process Configured Matches').classes('text-h4')

    preprocessed_files = file_processing.list_preprocessed_files()
    if not preprocessed_files:
        ui.label('No PreProcess_NewItems files found in Newfiletemp.')
        return

    file_select = ui.select(preprocessed_files, label='Select Preprocessed File')

    table = ui.aggrid()

    def load_file() -> None:
        selected_file = file_select.value
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

        table.options = {
            'columnDefs': [
                {'field': c} for c in df.columns
            ],
            'rowData': df.to_dict('records'),
            'editable': True,
        }
        table.update()
        _edit_store['key'] = selected_file

    file_select.on('update:model-value', load_file)

    def save_changes() -> None:
        if 'key' not in _edit_store:
            return
        df = table.options.get('rowData', [])
        _edit_store['df'] = pd.DataFrame(df)
        ui.notify('Changes saved. You can now download the updated file.')

    ui.button('Save Changes', on_click=save_changes)

    def download() -> None:
        df = _edit_store.get('df')
        name = _edit_store.get('key')
        if df is None or name is None:
            ui.notify('⚠️ Edit values and click "Save Changes" before downloading.', color='warning')
            return
        csv_data = df.to_csv(index=False).encode('utf-8')
        ui.download(data=csv_data, filename=f'updated_{name}')

    ui.button('Download CSV', on_click=download)

