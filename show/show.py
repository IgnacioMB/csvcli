import curses
import pandas as pd
from csvcli.functions import *
import math


filename = "/Users/ignacio/Downloads/pipe.csv"
ext = get_file_extension(filename)
format = get_format_from_file_extension(ext)
delimiter = guess_delimiter(filepath=filename)

df = read_file_to_df(filepath=filename,format=format,delimiter=delimiter)

df = df[['id', 'apartmenttype', 'isexpressbookable']].copy()


def get_partial_table_str(df, offset, row_count):

    limit = offset + row_count

    return pd_tabulate(df[offset:limit])


def show(stdscr):

    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()

    # determine the number of table rows that fit in the screen
    row_count = math.floor((sh - 3) / 2)
    offset = 0

    while True:

        stdscr.clear()
        stdscr.addstr(get_partial_table_str(df=df, offset=offset, row_count=row_count))
        stdscr.refresh()
        key = stdscr.get_wch()

        if key == curses.KEY_DOWN and offset < df.shape[0] -1:
            offset += 1

        if key == curses.KEY_UP and offset > 0:
            offset -= 1


if __name__ == "__main__":
    curses.wrapper(show)