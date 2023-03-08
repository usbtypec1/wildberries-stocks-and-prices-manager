from typing import Generator, Any

import PySimpleGUI as sg

__all__ = ('AppWindow',)


class AppWindow(sg.Window):

    def __init__(self):
        sg.theme('BluePurple')
        layout = [
            [
                sg.FileBrowse('Выбрать', target='-FILE-'),
                sg.Input(key='-FILE-', expand_x=True, tooltip='Путь до файла'),
            ],
            [
                sg.Input('API ключ', key='-API-KEY-INPUT-', expand_x=True, tooltip='API ключ'),
            ],
            [
                sg.Multiline(key='LOGS', expand_x=True, expand_y=True, visible=False, disabled=True),
            ],
            [
                sg.Button('Старт', expand_x=True, key='-START-'),
            ],
            [
                sg.Button('Сгенерировать шаблон', expand_x=True, key='-GENERATE-TEMPLATE-FILE-', pad=((5, 5), (10, 5))),
            ],
            [
                sg.Button('Выгрузить все цены', key='-DOWNLOAD-PRICES-', expand_x=True, pad=((5, 5), (10, 5))),
                sg.Button('Выгрузить все остатки', key='-DOWNLOAD-STOCKS-', expand_x=True, pad=((5, 5), (10, 5))),
            ],
        ]
        super().__init__(
            'Wildberries',
            layout,
            resizable=True,
            size=(400, 250),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def run(self) -> Generator[tuple[sg.Window, Any, Any], None, None]:
        while True:
            event, values = self.read()
            if event == sg.WIN_CLOSED:
                break
            yield event, values
