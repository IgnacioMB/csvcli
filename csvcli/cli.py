import click
from csvcli.functions import *


class CommonContext:
    def __init__(self, filepath, delimiter):
        self.filepath = filepath
        self.delimiter = delimiter


@click.group()
@click.pass_context
@click.option("-f", "--filepath", type=str, help="Path to the CSV file i.e. '~/Downloads/super_important_data.csv'.")
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
    display_table(filepath=common_ctx.obj.filepath, delimiter=common_ctx.obj.delimiter)


@cli.command()
@click.pass_context
def head(common_ctx):
    display_table(filepath=common_ctx.obj.filepath, delimiter=common_ctx.obj.delimiter, head=True)


@cli.command()
@click.pass_context
@click.option("-n", "--rowcount", type=int, help="Number of rows to show")
def nhead(common_ctx, rowcount):
    display_table(filepath=common_ctx.obj.filepath, delimiter=common_ctx.obj.delimiter, head=True, n=rowcount)


@cli.command()
@click.pass_context
def cols(common_ctx):
    display_columns(filepath=common_ctx.obj.filepath, delimiter=common_ctx.obj.delimiter)


@cli.command()
@click.pass_context
def describe(common_ctx):
    display_summary_stats(filepath=common_ctx.obj.filepath, delimiter=common_ctx.obj.delimiter)


@cli.command()
@click.pass_context
def nullcols(common_ctx):
    display_null_columns(filepath=common_ctx.obj.filepath, delimiter=common_ctx.obj.delimiter)







