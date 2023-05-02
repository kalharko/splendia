from curses import wrapper

from model.cli.cli_app import CliApp


def main(stdscr):
    stdscr.clear()
    app = CliApp(2, stdscr)


wrapper(main)
