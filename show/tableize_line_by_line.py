import sys
import pandas as pd
from csvcli.functions import *

filepath = "/Users/ignacio/Downloads/big_file.csv"
file_ext = get_file_extension(filepath)
format = get_format_from_file_extension(file_ext)
delimiter = guess_delimiter(filepath)


df = read_file_to_df(filepath=filepath, format=format, delimiter=delimiter)


def tableize(df):
    if not isinstance(df, pd.DataFrame):
        return

    df_columns = df.columns.tolist()
    max_len_in_lst = lambda lst: len(sorted(lst, reverse=True, key=len)[0])
    align_center = lambda st, sz: "{0}{1}{0}".format(" "*(1+(sz-len(st))//2), st)[:sz] if len(st) < sz else st
    align_right = lambda st, sz: "{0}{1} ".format(" "*(sz-len(st)-1), st) if len(st) < sz else st
    max_col_len = max_len_in_lst(df_columns)
    max_val_len_for_col = dict([(col, max_len_in_lst(df.iloc[:,idx].astype('str'))) for idx, col in enumerate(df_columns)])
    col_sizes = dict([(col, 2 + max(max_val_len_for_col.get(col, 0), max_col_len)) for col in df_columns])
    build_hline = lambda row: '+'.join(['-' * col_sizes[col] for col in row]).join(['+', '+'])
    build_data = lambda row, align: "|".join([align(str(val), col_sizes[df_columns[idx]]) for idx, val in enumerate(row)]).join(['|', '|'])
    hline = build_hline(df_columns)
    out = [hline, build_data(df_columns, align_center), hline]

    sys.stdout.write(hline)
    sys.stdout.write("\n")
    sys.stdout.write(build_data(df_columns, align_center))
    sys.stdout.write("\n")
    sys.stdout.write(hline)

    for index, row in df.iterrows():
        sys.stdout.write("\n")
        sys.stdout.write(build_data(row.tolist(), align_right))
        sys.stdout.write('\n')
        sys.stdout.write(hline)


tabulated = tableize(df.head())







