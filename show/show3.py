import curses
import pandas as pd
from csvcli.functions import *
import math


def get_table_str_from_df(df):
    return pd_tabulate(df)


def get_df_line_matrix_from_table_str(df_table_str):

    return df_table_str.split("\n")


def get_table_str_from_line_matrix(df_line_matrix):
    return '\n'.join(df_line_matrix)


def get_line_matrix_maxyx(df_line_matrix):

    th = len(df_line_matrix)

    # the width of the table is determined by its widest line
    tw = len(df_line_matrix[0])

    for line in df_line_matrix[1:]:
        if len(line) > tw:
            tw = len(line)

    return th, tw


def get_partial_line_matrix(df_line_matrix, sw, w_offset):

    df_partial_line_matrix = df_line_matrix

    th,tw = get_line_matrix_maxyx(df_line_matrix)

    # if the str matrix is wider than fits on screen
    # we only show as many chars as we can fit
    if tw + 1 > sw:
        for index in range(0, th):
            if len(df_partial_line_matrix[index]) > sw:
                df_partial_line_matrix[index] = df_partial_line_matrix[index][w_offset:w_offset+sw-1]

    return df_partial_line_matrix


filename = "/Users/ignacio/Downloads/region_name_last_snapshot.parquet"
ext = get_file_extension(filename)
format = get_format_from_file_extension(ext)
delimiter = guess_delimiter(filepath=filename)

df = read_file_to_df(filepath=filename,format=format,delimiter=delimiter)

#df = df[['id', 'apartmenttype', 'isexpressbookable']].copy()


def get_partial_table_str(df, row_count, sw, h_offset, w_offset):

    limit = h_offset + row_count

    df_table_str = pd_tabulate(df[h_offset:limit])

    df_line_matrix = get_df_line_matrix_from_table_str(df_table_str)

    th, tw = get_line_matrix_maxyx(df_line_matrix)

    partial_df_line_matrix = get_partial_line_matrix(df_line_matrix,sw,w_offset)

    partial_table_str = get_table_str_from_line_matrix(partial_df_line_matrix)

    return partial_table_str, tw


def show(stdscr):

    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()

    # determine the number of table rows that fit in the screen
    row_count = math.floor((sh - 3) / 2)
    h_offset = 0
    w_offset= 0

    w_step = 4

    while True:

        stdscr.clear()

        partial_table_str, tw = get_partial_table_str(df=df, row_count=row_count, sw=sw,
                                                  h_offset=h_offset, w_offset=w_offset)

        stdscr.addstr(partial_table_str)
        stdscr.refresh()
        key = stdscr.get_wch()

        if key == curses.KEY_DOWN and h_offset < df.shape[0] -1:
            h_offset += 1

        if key == curses.KEY_UP and h_offset > 0:
            h_offset -= 1

        if key == curses.KEY_LEFT and w_offset-w_step >= 0:
            w_offset -= w_step

        if key == curses.KEY_RIGHT and w_offset+w_step < tw-1:
            w_offset += w_step

        if key == 'q':
            break


if __name__ == "__main__":
    curses.wrapper(show)