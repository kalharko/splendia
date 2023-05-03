from curses import wrapper

from cli.cli_app import CliApp


def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    app = CliApp(2, stdscr)


wrapper(main)
