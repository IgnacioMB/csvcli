import os
import pandas as pd
import sys
from tabulate import tabulate
import click
import pandasql as psql
import numpy
from pandasql.sqldf import PandaSQLException


def get_filename(filepath):
    return os.path.splitext(filepath)[0]


def get_file_extension(filepath):
    return os.path.splitext(filepath)[1]


def assert_param(param, **kwargs):
    assert param in kwargs.keys(), f"Missing param: {param}!"


def check_path(original_function):
    def wrapper(*args, **kwargs):

        assert_param('filepath', **kwargs)

        # check if filepath exists
        if os.path.exists(kwargs['filepath']):
            return original_function(*args, **kwargs)
        else:
            print(f"\nOuch! Could not find '{kwargs['filepath']}'")
            sys.exit(0)

    return wrapper


def validate_delimiter(delimiter):
    if not isinstance(delimiter, str):
        print("\nError! CSV delimiter must be a string")
        sys.exit()

    if not len(delimiter) == 1:
        print("\nError! CSV delimiter must be a 1-character string")
        sys.exit()


def get_filepath_without_extension(filepath):
    current_file_ext = get_file_extension(filepath=filepath)
    return filepath[:-len(current_file_ext)]


def get_new_filepath(filepath, desired_format):

    filepath_wo_ext = get_filepath_without_extension(filepath=filepath)

    if desired_format == 'csv':
        return filepath_wo_ext + ".csv"

    elif desired_format == 'excel':
        return filepath_wo_ext + ".xlsx"

    elif desired_format == 'parquet':
        return filepath_wo_ext + ".parquet"

    else:
        print("Ouch! Invalid format choice. You need to choose between 'csv', 'excel' or 'parquet'.")


def output_to_file(*args, **kwargs):
    """
    Outputs a DataFrame in the desired format
    :param df: Pandas DataFrame
    :param filepath: path where the output file will be stored example '/Users/john/Downloads/mydir/myfile.csv'
    :param delimiter: (optional) csv delimiter if you want to output in csv with other than comma
    :param desired_format: has to be 'csv', 'excel' or 'parquet'
    :return:
    ------------------------------------------------------------------------
    Code sample
    ------------------------------------------------------------------------
    format_change(filepath='/Users/john/Downloads/mydir/myfile.csv',
                  delimiter=';',
                  desired_format='excel')
    """

    assert_param('df', **kwargs)
    assert_param('filepath', **kwargs)
    assert_param('desired_format', **kwargs)

    if kwargs['desired_format'] == 'csv':
        if 'delimiter' in kwargs.keys() and kwargs['delimiter'] is not None:
            kwargs['df'].to_csv(kwargs['filepath'], sep=kwargs['delimiter'], index=False)
        else:
            kwargs['df'].to_csv(kwargs['filepath'], index=False)

    elif kwargs['desired_format'] == 'excel':
        kwargs['df'].to_excel(kwargs['filepath'], index=False)

    elif kwargs['desired_format'] == 'parquet':
        kwargs['df'].to_parquet(kwargs['filepath'], index=False)

    else:
        print("Ouch! Invalid format choice. You need to choose between 'csv', 'excel' or 'parquet'.")


@check_path
def delete_local_file(filepath):
    os.remove(filepath)


def pd_tabulate(my_df):
    return tabulate(my_df, headers='keys', tablefmt='fancy_grid')


def get_col_list(col_string):

    # convert input str into list of columns
    col_list = col_string.split(',')

    # discard any potential trailing and leading white spaces generated by user input
    col_list = [x.strip(' ') for x in col_list].copy()

    return col_list


def get_format_from_file_extension(file_extension):

    if file_extension == '.csv':
        format = 'csv'

    elif file_extension == '.parquet':
        format = 'parquet'

    elif file_extension in ['.xlsx', '.xls']:
        format = 'excel'

    else:
        print("Ouch! csvcli can only process CSV, excel and parquet files")
        sys.exit(0)

    return format


@check_path
def read_file_to_df(filepath, delimiter=','):

    file_extension = get_file_extension(filepath=filepath)

    format = get_format_from_file_extension(file_extension=file_extension)

    if format == 'csv':
        df = pd.read_csv(filepath, delimiter=delimiter)

    elif format == 'parquet':
        df = pd.read_parquet(filepath)

    elif format == 'excel':
        df = pd.read_excel(filepath)

    return df


def filter_df(df, head=False, n=None, columns=None, sort_by=None, ascending=True):

    output_df = df.copy()

    if columns is not None:

        col_list = get_col_list(col_string=columns)

        for col in col_list:
            if col not in output_df.columns:
                print(f"Ouch! Column '{col}' does not seem to be in your file...")
                sys.exit(0)

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
    # We also cast dictionaries and dates into str to be on the safe side

    not_supported_types = [numpy.ndarray, list, tuple, set, dict, numpy.datetime64]

    bad_columns = [col for col in df.columns if get_dtype(df[col]) in not_supported_types]

    for col in bad_columns:
        df[col] = df[col].astype(str)

    return df


def filter_df_by_query(df, query):

    file = get_df_casted_to_supported_types(df)

    # if the column names contain spaces, convert them to underscores so you can still query them
    file.columns = [col.replace(' ', '_') for col in file.columns]

    try:
        result_df = psql.sqldf(query, {**locals(), **globals()})

    except PandaSQLException as e:

        error = e.__str__().split('\n')[0]

        print(f"Ouch! Your SQL query failed: {error}")

        sys.exit(0)

    return result_df


def get_value_counts(df, column):

    result = pd.DataFrame(df[column].value_counts()).reset_index()
    result.rename(columns={'index': 'unique_value', column: f'count'}, inplace=True)

    return result


