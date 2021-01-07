import curses
import pandas as pd
from csvcli.functions import *
import math
import unicodedata


def get_clean_df(df):

    # remove new line chars from df values to ensure each row is one line
    return df.replace(r'\n', ' ', regex=True).copy()


def get_table_str_from_df(df, repl_for_wide='?'):

    table_str = pd_tabulate(df)

    # replace wide chars
    table_str = ''.join([char if unicodedata.east_asian_width(char) != 'W' else repl_for_wide for char in table_str])

    return table_str


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


def get_partial_table_str(df, row_count, sw, h_offset, w_offset):

    limit = h_offset + row_count

    df = df[h_offset:limit].copy()

    df = get_clean_df(df).copy()

    df_table_str = get_table_str_from_df(df)

    df_line_matrix = get_df_line_matrix_from_table_str(df_table_str)

    th, tw = get_line_matrix_maxyx(df_line_matrix)

    partial_df_line_matrix = get_partial_line_matrix(df_line_matrix,sw,w_offset)

    partial_table_str = get_table_str_from_line_matrix(partial_df_line_matrix)

    return partial_table_str, tw


def get_filled_header(msg, width, fill_char):
    assert len(msg) <= width, "your message does not fit!"
    array_msg = [char for char in msg]
    array = [fill_char] * width
    array[(width // 2 - len(msg) // 2): (width // 2 - len(msg) // 2) + (len(msg))] = array_msg
    return "".join(array)


def display_meta_info(stdscr, full_filename, format, delimiter, is_delimiter_a_guess, df, display_type, query=""):

    sh, sw = stdscr.getmaxyx()

    total_lines = 3

    file_name_msg = f"FILENAME: {full_filename}"
    header = get_filled_header(msg=file_name_msg, width=sw, fill_char=" ")

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(0,0,header)
    stdscr.attroff(curses.color_pair(1))

    if format == 'csv' and delimiter != ',' and is_delimiter_a_guess and not display_type == "query":
        stdscr.addstr(2,1,f"Infered CSV Delimiter: '{delimiter}'")
        total_lines +=1

    query_msg = f"QUERY: '{query}'"

    if display_type == "query":
        if len(query_msg) + 1 < sw:
            stdscr.addstr(2, 1, query_msg)
        else:
            stdscr.addstr(2, 1, query_msg[:sw])
        total_lines += 1

    if display_type == "all":
        msg_total_number = f"Total number of rows: {df.shape[0]}"

    elif display_type == "head":
        msg_total_number = f"Number of rows displayed: {df.shape[0]}"

    elif display_type in ["columns", "null_counts"]:
        msg_total_number = f"Total number of columns: {df.shape[0]}"

    elif display_type == "value_counts":
        msg_total_number = f"Total number of unique values: {df.shape[0]}"

    elif display_type == "query":
        msg_total_number = f"Rows in query result: {df.shape[0]}"

    elif display_type == "select":
        msg_total_number = f"Total number of rows in selection: {df.shape[0]}"

    else:
        msg_total_number = f""

    stdscr.addstr(curses.LINES - 2, 1, msg_total_number)

    quit_footer = "PRESS 'Q' TO QUIT"

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(curses.LINES - 2, sw//2 - len(quit_footer)//2, quit_footer)
    stdscr.attroff(curses.color_pair(1))

    return total_lines


def display_full_table(stdscr, full_filename, format, df, display_type,
                       query="", is_delimiter_a_guess=None, delimiter=None):

    curses.curs_set(0)
    h_offset = 0
    w_offset = 0

    w_step = 4

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True:

        stdscr.clear()

        sh, sw = stdscr.getmaxyx()

        h_padding = display_meta_info(stdscr, full_filename, format, delimiter, is_delimiter_a_guess, df, display_type, query)

        # determine the number of table rows that fit in the screen
        row_count = math.floor((sh - 3) / 2) - h_padding

        partial_table_str, tw = get_partial_table_str(df=df, row_count=row_count, sw=sw-10,
                                                      h_offset=h_offset, w_offset=w_offset)

        stdscr.addstr(h_padding, 0, partial_table_str)
        stdscr.refresh()
        key = stdscr.get_wch()

        if key == curses.KEY_DOWN and (h_offset + 1) <= (df.shape[0] - row_count):
            h_offset += 1

        if key == curses.KEY_UP and h_offset > 0:
            h_offset -= 1

        if key == curses.KEY_LEFT and w_offset-w_step >= 0:
            w_offset -= w_step

        if key == curses.KEY_RIGHT and w_offset+w_step < tw-1:
            w_offset += w_step

        if key == 'a' or key == 'A':
            h_offset = 0

        if key == 'z' or key == 'Z':
            h_offset = df.shape[0] - row_count

        if key == 'q' or key == 'Q':
            break

        resize = curses.is_term_resized(sh, sw)

        # Action in loop if resize is True:
        if resize is True:
            sh, sw = stdscr.getmaxyx()
            stdscr.clear()
            curses.resizeterm(sh, sw)
            stdscr.refresh()


if __name__ == "__main__":

    filename = "/Users/ignacio/Downloads/region_name_last_snapshot.parquet"
    ext = get_file_extension(filename)
    full_filename = filename + ext
    format = get_format_from_file_extension(ext)
    is_delimiter_a_guess = False
    delimiter = guess_delimiter(filepath=filename)
    if delimiter is not None:
        is_delimiter_a_guess = True

    df = read_file_to_df(filepath=filename, format=format, delimiter=delimiter)

    curses.wrapper(display_full_table, full_filename, format, is_delimiter_a_guess, delimiter, df)