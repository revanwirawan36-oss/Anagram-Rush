import curses

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Tekan apa saja untuk keluar...")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)