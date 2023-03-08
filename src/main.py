import logging

from ui.controller import handle_event
from ui.view import AppWindow


def main():
    logging.basicConfig(level=logging.INFO)
    with AppWindow() as app_window:
        for event, values in app_window.run():
            handle_event(app_window, event, values)


if __name__ == '__main__':
    main()
