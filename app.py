from nicegui import ui
from frontend import config_page, main_page, configure_matching, process_configured_matches


def navbar():
    with ui.header().classes('justify-between'):
        ui.label('Maggys Order App')
        with ui.row():
            ui.link('Configure matching', '/configure')
            ui.link('Pre-process matching', '/')
            ui.link('Process configured matches', '/process')


@ui.page('/')
def index_page() -> None:
    navbar()
    main_page.main_page()


@ui.page('/configure')
def configure_page() -> None:
    navbar()
    configure_matching.configure_matching_page()


@ui.page('/process')
def process_page() -> None:
    navbar()
    process_configured_matches.process_configured_matches_page()


ui.run(title='Maggys Order App')
