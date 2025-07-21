# frontend/upload_page.py
from nicegui import ui
from config import paths
import shutil


def upload_page() -> None:
    ui.label('Upload PO File').classes('text-h4')

    def handle_upload(e) -> None:
        save_path = paths.UPLOADED_PO_DIR / e.name
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(e.content, f)
        ui.notify(f'File {e.name} uploaded successfully!')

    ui.upload(on_upload=handle_upload).props('accept=.xlsx')
