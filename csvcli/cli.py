import click
from csvcli.functions import *


class CommonContext:
    def __init__(self, filepath, delimiter):
        self.filepath = filepath
        self.delimiter = delimiter
        if filepath is not None:
            self.filename = get_filename(filepath=filepath)
            self.file_extension = get_file_extension(filepath=filepath)
            self.df = read_file_to_df(filepath=filepath, delimiter=delimiter)


@click.group()
@click.pass_context
@click.option("-f", "--filepath", type=str, help="Path to the file i.e. '~/Downloads/super_important_data.csv'.")
@click.option("-d", "--delimiter", type=str, help="Delimiter of the CSV file i.e. ';'. Must be a 1-character string.")
def cli(common_ctx, filepath, delimiter):
    """Welcome to csvcli, a simple command-line interface to work with CSV files!"""
    common_ctx.obj = CommonContext(filepath, delimiter)


"""
EXPLORE YOUR DATA         
"""

@cli.command()
@click.pass_context
def show(common_ctx):
    display_df(df=common_ctx.obj.df)


@cli.command()
@click.pass_context
@click.option("-n", "--rowcount", type=int, help="Number of rows to show")
def head(common_ctx, rowcount):
    common_ctx.obj.df = filter_df(df=common_ctx.obj.df, head=True, n=rowcount).copy()
    display_df(df=common_ctx.obj.df)


@cli.command()
@click.pass_context
def columns(common_ctx):

    display_df(get_dtypes(df=common_ctx.obj.df, pretty=True))


@cli.command()
@click.pass_context
def describe(common_ctx):
    display_df(get_summary_stats(df=common_ctx.obj.df))


@cli.command()
@click.pass_context
def null_counts(common_ctx):
    display_df(get_null_columns(df=common_ctx.obj.df))


@cli.command()
@click.pass_context
@click.option("-c", "--column", type=str, help="Name of column to count the unique values for")
def value_counts(common_ctx, column):
    display_df(get_value_counts(df=common_ctx.obj.df, column=column))


"""
FILTER AND QUERY
"""


@cli.command()
@click.pass_context
@click.option("-c", "--columns", type=str, help="Names of columns to show separated by commas")
@click.option("-s", "--sort_by", type=str, help="Name of column to sort by")
@click.option("-asc", "--ascending", type=bool, help="bool True for ascending and False for descending")
@click.option("-save", "--save_to", type=str, help="Destination path i.e. '~/Downloads/my_query.csv'. The file extension of your destination path determines output format")
def select(common_ctx, columns, sort_by, ascending, save_to):

    common_ctx.obj.df = filter_df(df=common_ctx.obj.df, columns=columns, sort_by=sort_by, ascending=ascending).copy()

    # we show result on screen if not save selected
    if save_to is None:

        display_df(df=common_ctx.obj.df)

    # if save selected, do not show result on screen, just write to file and confirm
    else:

        file_ext = get_file_extension(save_to)
        format = get_format_from_file_extension(file_extension=file_ext)

        output_to_file(df=common_ctx.obj.df,
                       filepath=save_to,
                       desired_format=format)

        print(f"successfully wrote select result into {save_to}")


@cli.command()
@click.pass_context
@click.option("-q", "--query", type=str, help="SQL query you want to run against the file")
@click.option("-save", "--save_to", type=str, help="Destination path i.e. '~/Downloads/my_query.csv'. The file extension of your destination path determines output format")
def query(common_ctx, query, save_to):

    common_ctx.obj.df = filter_df_by_query(df=common_ctx.obj.df, query=query).copy()

    # we show result on screen if not save selected
    if save_to is None:

        display_df(df=common_ctx.obj.df)

    # if save selected, do not show result on screen, just write to file and confirm
    else:

        file_ext = get_file_extension(save_to)
        format = get_format_from_file_extension(file_extension=file_ext)

        output_to_file(df=common_ctx.obj.df,
                       filepath=save_to,
                       desired_format=format)

        print(f"successfully wrote query result into {save_to}")


"""
CHANGE THE FORMAT
"""


@cli.command()
@click.pass_context
@click.option("-to", "--format", type=str, help="Output format. Options: 'csv', 'excel' or 'parquet'")
@click.option("-D", "--delimiter", type=str, help="Output CSV delimiter i.e. ';'. Must be a 1-character string")
def convert(common_ctx, format, delimiter):

    new_filepath = get_new_filepath(filepath=common_ctx.obj.filepath, desired_format=format)

    # if the new format is different from the original one
    if get_file_extension(filepath=new_filepath) != common_ctx.obj.file_extension:

        output_to_file(df=common_ctx.obj.df,
                       filepath=new_filepath,
                       desired_format=format,
                       delimiter=delimiter)

        delete_local_file(filepath=common_ctx.obj.filepath)

        print(f"successfully converted {common_ctx.obj.filepath} to '{format}'")

    else:
        print("Ouch! The original formal of the file and the new format you selected are identical")


@cli.command()
@click.pass_context
@click.option("-D", "--new_delimiter", type=str, help="Output CSV delimiter i.e. ';'. Must be a 1-character string")
def change_delimiter(common_ctx, new_delimiter):

    if common_ctx.obj.filepath.endswith('.csv'):
        output_to_file(df=common_ctx.obj.df,
                       filepath=common_ctx.obj.filepath,
                       desired_format='csv',
                       delimiter=new_delimiter)

        print(f"successfully changed CSV delimiter of {common_ctx.obj.filepath} to '{new_delimiter}'")

    else:
        print("Ouch! You can only change delimiter of CSV files")