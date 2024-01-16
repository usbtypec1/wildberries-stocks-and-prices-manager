from rich.console import Console

import cli
from database.base import create_tables


def main():
    create_tables()
    console = Console(log_path=False)
    cli.run(console)


if __name__ == '__main__':
    main()
