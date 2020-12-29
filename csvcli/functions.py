import os
import pandas as pd
import sys
from tabulate import tabulate
import click
import pandasql as psql
import numpy


def assert_param(param, **kwargs):
    assert param in kwargs.keys(), f"Missing param: {param}!"


def get_full_local_path(local_directory, filename):

    # generate full path to file depending on ending char of local_directory
    if local_directory[-1] != "/":
        full_local_path = local_directory + "/" + filename
    else:
        full_local_path = local_directory + filename

    return full_local_path


def check_local_dir_and_file(original_function):
    def wrapper(*args, **kwargs):

        assert_param('local_directory', **kwargs)
        assert_param('filename', **kwargs)

        # check if directory exists
        if os.path.exists(kwargs['local_directory']):
            full_local_path = get_full_local_path(kwargs['local_directory'], kwargs['filename'])

            # check if file exists within directory
            if os.path.exists(full_local_path):
                original_function(*args, **kwargs)

            else:
                print(f"\nOuch! There is no file called '{kwargs['filename']}' in {kwargs['local_directory']}")

        else:
            print(f"\nOuch! This local directory does not exist {kwargs['local_directory']}")

    return wrapper


def validate_delimiter(csv_delimiter):
    if not isinstance(csv_delimiter, str):
        print("\nError! CSV delimiter must be a string")
        sys.exit()

    if not len(csv_delimiter) == 1:
        print("\nError! CSV delimiter must be a 1-character string")
        sys.exit()


@check_local_dir_and_file
def local_delimiter_change(*args, **kwargs):
    """
    Changes the delimiter of a local file
    :param filename: name of the file example 'myfile.csv'
    :param local_directory: path to the directory where the file is stored example '/Users/john/Downloads/mydir'
    :param old_delimiter: example ','
    :param new_delimiter: example ';'
    :return:
    ------------------------------------------------------------------------
    Code sample
    ------------------------------------------------------------------------
    local_delimiter_change(filename='Seo_Pages_Data_(2020-12-19).csv',
                           local_directory='/Users/john/Downloads',
                           old_delimiter=';', new_delimiter='|')
    """

    assert_param('filename', **kwargs)
    assert_param('local_directory', **kwargs)
    assert_param('old_delimiter', **kwargs)
    assert_param('new_delimiter', **kwargs)

    validate_delimiter(kwargs['old_delimiter'])
    validate_delimiter(kwargs['new_delimiter'])


    # read original csv
    full_local_path = get_full_local_path(kwargs['local_directory'], kwargs['filename'])
    df = pd.read_csv(full_local_path, sep=kwargs['old_delimiter'])

    # overwrite with new delimiter
    df.to_csv(full_local_path, sep=kwargs['new_delimiter'], index=False)

    print(f"successfully changed delimiter of '{full_local_path}' from '{kwargs['old_delimiter']}' to '{kwargs['new_delimiter']}'")


def get_parquet_filename(filename):
    return filename[:-4] + ".parquet"


@check_local_dir_and_file
def local_csv_to_parquet(*args, **kwargs):
    """
    Transforms a local CSV file to parquet
    :param filename: name of the file example 'myfile.csv'
    :param local_directory: path to the directory where the file is stored example '/Users/john/Downloads/mydir'
    :param csv_delimiter: example ';'
    :param keep_original: boolean to indicate if you want to keep the original file, if False you delete the csv
    :return:
    ------------------------------------------------------------------------
    Code sample
    ------------------------------------------------------------------------
    local_csv_to_parquet(filename='bookings.csv',
                         local_directory='/Users/john/Downloads/bookings',
                         keep_original=True,
                         csv_transform=';')
    """

    assert_param('filename', **kwargs)
    assert_param('local_directory', **kwargs)
    assert_param('csv_transform', **kwargs)
    assert_param('keep_original', **kwargs)

    print(f"convert: {kwargs['filename']} to parquet...")

    # read original csv
    csv_full_local_path = get_full_local_path(kwargs['local_directory'], kwargs['filename'])
    df = pd.read_csv(csv_full_local_path, sep=kwargs['csv_transform'])

    # write parquet
    parquet_filename = get_parquet_filename(kwargs['filename'])
    parquet_full_local_path = get_full_local_path(kwargs['local_directory'], parquet_filename)
    df.to_parquet(parquet_full_local_path, index=False)

    # delete original if asked for it
    if not kwargs['keep_original']:
        os.remove(csv_full_local_path)


def get_list_of_csv_files_in_local_directory(local_directory):

    os.system(f"ls -l {local_directory} > files.txt")
    with open("files.txt", mode='r') as myfile:
        ls_file = myfile.readlines()
    file_list = list(map(lambda x: x.split(' ')[-1][:-1], ls_file[1:]))
    file_list = list(filter(lambda x: x.endswith(".csv"), file_list))
    os.remove('files.txt')

    return file_list


def apply_to_all_csv_files_in_local_dir(original_function):

    """
    Pre-Requisites:
        -CSV filenames cannot contain spaces!!
    """

    def wrapper(*args, **kwargs):

        assert_param('local_directory', **kwargs)

        if os.path.exists(kwargs['local_directory']):

            # generate list of all CSV files in directory
            file_list = get_list_of_csv_files_in_local_directory(kwargs['local_directory'])

            print(f"\nTotal number of CSV files in {kwargs['local_directory']}: {len(file_list)}")

            # apply original function to each CSV file
            i = 1
            for filename in file_list:
                print(f"\n({i}/{len(file_list)})")
                new_kwargs = kwargs.copy()
                new_kwargs['filename'] = filename
                original_function(*args, **new_kwargs)
                i += 1

        else:
            print(f"\nOuch! This path does not exist {kwargs['local_directory']}")

    return wrapper


local_change_delimiter_whole_dir = apply_to_all_csv_files_in_local_dir(local_delimiter_change)

local_change_delimiter_whole_dir.__doc__ = """
Changes the delimiter of all the csv files within the directory indicated by local_directory
Ignores non-csv files
Pre-Requisites:
    -All original CSV files must have the same delimiter
    -CSV filenames cannot contain spaces!!
:param local_directory: path to the directory where the files are stored example '/Users/john/Downloads/mydir'
:param old_delimiter: example ','
:param new_delimiter: example ';'
:return:
------------------------------------------------------------------------
Code sample
------------------------------------------------------------------------
local_change_delimiter_whole_dir(local_directory='/Users/john/Downloads/bookings',
                                 old_delimiter=',', new_delimiter='|')
"""

local_csv_to_parquet_whole_dir = apply_to_all_csv_files_in_local_dir(local_csv_to_parquet)

local_csv_to_parquet_whole_dir.__doc__ = """
    Transforms to parquet all the CSV files within the directory indicated by local_directory
    Ignores non-csv files
    Pre-Requisites:
        -All original CSV files must have the same delimiter
        -CSV filenames cannot contain spaces!!
    :param local_directory: path to the directory where the files are stored example '/Users/john/Downloads/mydir'
    :param keep_original: boolean to indicate if you want to keep the original files, if False you delete the csv files
    :param csv_transform: example ';'
    :return:
    ------------------------------------------------------------------------
    Code sample
    ------------------------------------------------------------------------
    local_csv_to_parquet_whole_dir(keep_original=True, csv_transform=';',
                                   local_directory='/Users/john/Downloads/bookings')
    """


@check_local_dir_and_file
def delete_local_file(filename, local_directory):
    full_local_path = get_full_local_path(local_directory, filename)
    print(f"delete: {full_local_path}...")
    os.remove(full_local_path)


def pd_tabulate(my_df):
    return tabulate(my_df, headers='keys', tablefmt='fancy_grid')


def get_col_list(col_string):

    # convert input str into list of columns
    col_list = col_string.split(',')

    # discard any potential trailing and leading white spaces generated by user input
    col_list = [x.strip(' ') for x in col_list].copy()

    return col_list


def read_file_to_df(filepath, delimiter=','):

    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, delimiter=delimiter)

    elif filepath.endswith('.parquet'):
        df = pd.read_parquet(filepath)

    elif filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)

    return df


def filter_df(df, head=False, n=None, columns=None, sort_by=None, ascending=True):

    output_df = df.copy()

    if columns is not None:
        col_list = get_col_list(col_string=columns)
        output_df = df[col_list].copy()

    if sort_by is not None:
        output_df = output_df.sort_values(by=sort_by, ascending=ascending)

    if head:
        if n is not None:
            output_df = output_df.head(n)
        else:
            output_df = output_df.head()

    return output_df


def display_df(df):
    click.echo(pd_tabulate(df))


def get_dtype(series, pretty=False):
    series = series[series.notna()].copy()

    if series.shape[0] > 0:

        if pretty:
            return type(series.head(1).values[0]).__name__

        else:
            return type(series.head(1).values[0])

    else:
        return None


def get_dtypes(df, pretty=False):

    type_dict_list = [{"column_name": col, 'data_type': get_dtype(df[col], pretty)} for col in df.columns]

    return pd.DataFrame(type_dict_list)


def get_summary_stats(df):

    return df.describe()


def get_null_columns(df):

    null_df = df.isna().sum().reset_index().rename(columns={'index': 'column_name', 0: 'count_of_nulls'})

    return null_df


def get_df_casted_to_supported_types(df):

    # pandasql uses SQLite syntax
    # SQLite does not support arrays
    # In order to not have the query crash whenever an array is in the query result we need to cast arrays into strings

    not_supported_types = [numpy.ndarray, list, tuple, set]

    bad_columns = [col for col in df.columns if get_dtype(df[col]) in not_supported_types]

    for col in bad_columns:
        df[col] = df[col].astype(str)

    return df


def filter_df_by_query(df, query):

    file = get_df_casted_to_supported_types(df)

    result_df = psql.sqldf(query, {**locals(), **globals()})

    return result_df


def get_value_counts(df, column):

    result = pd.DataFrame(df[column].value_counts()).reset_index()
    result.rename(columns={'index': 'unique_value', column: f'count'}, inplace=True)

    return result


