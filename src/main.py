from rich.console import Console

import cli


def main():
    console = Console(log_path=False)
    cli.run(console)


if __name__ == '__main__':
    main()
