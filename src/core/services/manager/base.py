from rich.console import Console

__all__ = ('ManagerService',)


class ManagerService:

    def __init__(self, console: Console, token: str):
        self._console = console
        self._token = token
