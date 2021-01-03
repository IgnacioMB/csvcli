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


def get_partial_line_matrix(df_line_matrix, sh, sw, h_offset, w_offset):

    df_partial_line_matrix = df_line_matrix

    th,tw = get_line_matrix_maxyx(df_line_matrix)

    # if the str matrix has more lines than they fit onscreen,
    # we take only as many as fit starting from height offset
    if th > sh:
        df_partial_line_matrix = df_partial_line_matrix[h_offset: h_offset+sh]
        th = len(df_partial_line_matrix)

    # if the str matrix is wider than fits on screen
    # we only show as many chars as we can fit
    if tw + 1 > sw:
        for index in range(0, th):
            if len(df_partial_line_matrix[index]) > sw:
                df_partial_line_matrix[index] = df_partial_line_matrix[index][w_offset:w_offset+sw-1]

    return df_partial_line_matrix

filename = "/Users/ignacio/Downloads/pipe.csv"
ext = get_file_extension(filename)
format = get_format_from_file_extension(ext)
delimiter = guess_delimiter(filepath=filename)

df = read_file_to_df(filepath=filename,format=format,delimiter=delimiter)
df = df.head(100).copy()
#df = df[['id', 'apartmenttype', 'isexpressbookable']].copy()


print()

def show(stdscr):

    curses.curs_set(0)

    sh, sw = stdscr.getmaxyx()

    df_table_str = get_table_str_from_df(df)

    h_padding = 1


    h_offset = 0
    w_offset = 0

    h_step = 1
    w_step = 4

    while True:

        stdscr.clear()

        df_line_matrix = get_df_line_matrix_from_table_str(df_table_str)
        th, tw = get_line_matrix_maxyx(df_line_matrix)
        partial_line_matrix = get_partial_line_matrix(df_line_matrix, sh-h_padding, sw, h_offset, w_offset)
        partial_df_string = get_table_str_from_line_matrix(partial_line_matrix)

        stdscr.addstr(0+h_padding,0,partial_df_string)
        stdscr.refresh()

        key = stdscr.get_wch()

        if key == curses.KEY_DOWN and h_offset + h_step < th-1:
            h_offset += h_step

        if key == curses.KEY_UP and h_offset-h_step >= 0:
            h_offset -= h_step

        if key == curses.KEY_LEFT and w_offset-w_step >= 0:
            w_offset -= w_step

        if key == curses.KEY_RIGHT and w_offset+w_step < tw-1:
            w_offset += w_step

        if key == 'q':
            break


if __name__ == "__main__":
    curses.wrapper(show)