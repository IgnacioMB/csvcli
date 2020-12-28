import click
from csvcli.functions import *


class CommonContext:
    def __init__(self, filepath, delimiter):
        self.filepath = filepath
        self.delimiter = delimiter
        if filepath is not None:
            self.df = read_file_to_df(filepath=filepath, delimiter=delimiter)


@click.group()
@click.pass_context
@click.option("-f", "--filepath", type=str, help="Path to the file i.e. '~/Downloads/super_important_data.csv'.")
@click.option("-d", "--delimiter", type=str, help="Delimiter of the CSV file i.e. ','. Must be a 1-character string.")
def cli(common_ctx, filepath, delimiter):
    """Welcome to csvcli, a simple command-line interface to work with CSV files!"""
    common_ctx.obj = CommonContext(filepath, delimiter)


@cli.command()
@click.pass_context
@click.option("-D", "--new_delimiter", type=str, help="Output CSV delimiter i.e. ';'. Must be a 1-character string")
def change_delimiter(common_ctx, new_delimiter):

    filename = common_ctx.obj.filepath.split("/")[-1]
    local_directory = "/".join(common_ctx.obj.filepath.split("/")[:-1])

    local_delimiter_change(filename=filename,
                           local_directory=local_directory,
                           old_delimiter=common_ctx.obj.delimiter,
                           new_delimiter=new_delimiter)


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

    display_df(get_column_names(df=common_ctx.obj.df))


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
@click.option("-c", "--columns", type=str, help="Names of columns to show separated by commas")
@click.option("-s", "--sort_by", type=str, help="Name of column to order by")
@click.option("-asc", "--ascending", type=bool, help="bool True for ascending and False for descending")
def select(common_ctx, columns, sort_by, ascending):

    common_ctx.obj.df = filter_df(df=common_ctx.obj.df, columns=columns, sort_by=sort_by, ascending=ascending).copy()
    display_df(df=common_ctx.obj.df)


@cli.command()
@click.pass_context
@click.option("-q", "--query", type=str, help="SQL query you want to run against the file")
def query(common_ctx, query):
    common_ctx.obj.df = filter_df_by_query(df=common_ctx.obj.df, query=query).copy()
    display_df(df=common_ctx.obj.df)
