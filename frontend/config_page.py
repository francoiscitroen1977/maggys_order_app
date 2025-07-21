# frontend/config_page.py
from nicegui import ui
from config import config_manager, paths
from services import file_processing
import shutil

def config_page() -> None:
    ui.label('Configuration').classes('text-h4')

    config = config_manager.load_config()

    new_items_files = file_processing.list_files_in_directory(paths.NEW_ITEMS_DIR)
    po_files = file_processing.list_files_in_directory(paths.UPLOADED_PO_DIR)

    def handle_upload(e) -> None:
        save_path = paths.UPLOADED_PO_DIR / e.name
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(e.content, f)
        ui.notify(f'File {e.name} uploaded successfully!')
        po_select.options = file_processing.list_files_in_directory(paths.UPLOADED_PO_DIR)

    ui.upload(on_upload=handle_upload).props('accept=.xlsx').label('Upload PO File')

    new_select = ui.select(new_items_files, value=config.get('newitems_file'), label='Select New Items File')
    po_select = ui.select(po_files, value=config.get('po_files', []), label='Select PO Files', multiple=True)

    logging_checkbox = ui.checkbox('Logging On', value=config.get('logging_on', False))

    if po_files and len(config.get('po_files', [])) == 0:
        ui.notify('Please select at least one PO file before saving.', color='warning')

    po_qty_input = ui.input(label='PO Quantity Column Name', value=config.get('po_qty_column', 'Sales Products Qty'))

    if len(po_files) == 0:
        ui.notify('No PO files available. Please upload a PO file before saving.', color='warning')

    def save_config() -> None:
        config['newitems_file'] = new_select.value
        config['po_files'] = po_select.value if isinstance(po_select.value, list) else []
        config['logging_on'] = logging_checkbox.value
        config['po_qty_column'] = po_qty_input.value
        config_manager.save_config(config)
        ui.notify('Configuration Saved!')

    ui.button('Save Configuration', on_click=save_config, disabled=len(po_files) == 0 or len(config.get('po_files', [])) == 0)
