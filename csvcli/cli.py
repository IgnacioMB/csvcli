import click
from csvcli.functions import *


class CommonContext:
    def __init__(self, filepath, delimiter):
        self.filepath = filepath
        self.delimiter = delimiter
        self.filename = get_filename(filepath=filepath)
        self.file_extension = get_file_extension(filepath=filepath)
        self.df = read_file_to_df(filepath=filepath, delimiter=delimiter)


@click.group()
@click.pass_context
@click.argument("filepath", type=str, required=True)
@click.option("-d", "--delimiter", type=str, help="(optional) Only for CSV files. Delimiter if other than comma i.e. ';'. Must be a 1-character string.")
def cli(common_ctx, filepath, delimiter):
    """

    WELCOME to csvcli, a simple command-line interface to work with CSV, excel and parquet files.

    You can use it to:

    - Explore your data: navigate through the full contents of your tabular data fast and with a human-friendly format directly on the shell.
      Quickly see which columns, data-types are in the file and how many null values or unique values are per column.

    - Filter and query: select subsets of the tabular data, sort by a given column... Need more? Ok then just run SQL queries on it! In all cases you can save the output to a new file

    - Change the format: you can convert from and to CSV, excel and parquet in any combination. You can change the delimiter of your CSV file

    Full documentation with examples: https://github.com/IgnacioMB/csvcli

    """

    common_ctx.obj = CommonContext(filepath, delimiter)


"""
EXPLORE YOUR DATA         
"""


@cli.command()
@click.pass_context
def show(common_ctx):
    """
    Displays the contents of the CSV, excel or parquet file.
    """

    click.echo(f"\nFilename: {common_ctx.obj.filename+common_ctx.obj.file_extension} \nTotal number of rows: {common_ctx.obj.df.shape[0]}\n")
    paginated_display(df=common_ctx.obj.df, filename=common_ctx.obj.filename+common_ctx.obj.file_extension, chunksize=5000)


@cli.command()
@click.pass_context
@click.argument("rowcount", type=int, default=5, required=False)
def head(common_ctx, rowcount):
    """
    Displays only the first rows of the file.
    """
    click.echo(f"\nFilename: {common_ctx.obj.filename + common_ctx.obj.file_extension} \nTotal number of rows: {common_ctx.obj.df.shape[0]}\n")
    common_ctx.obj.df = filter_df(df=common_ctx.obj.df, head=True, n=rowcount).copy()
    display_df(df=common_ctx.obj.df)


@cli.command()
@click.pass_context
def columns(common_ctx):
    """
    Displays the column names and data types of the file.
    """
    click.echo(f"\nFilename: {common_ctx.obj.filename + common_ctx.obj.file_extension} \nTotal number of rows: {common_ctx.obj.df.shape[0]}\n")
    display_df(get_dtypes(df=common_ctx.obj.df, pretty=True))


@cli.command()
@click.pass_context
def describe(common_ctx):
    """
    Displays a table with summary statistics.
    """
    click.echo(f"\nFilename: {common_ctx.obj.filename + common_ctx.obj.file_extension} \nTotal number of rows: {common_ctx.obj.df.shape[0]}\n")
    display_df(get_summary_stats(df=common_ctx.obj.df))


@cli.command()
@click.pass_context
def null_counts(common_ctx):
    """
    Displays the counts of null values per column.
    """
    click.echo(f"\nFilename: {common_ctx.obj.filename + common_ctx.obj.file_extension} \nTotal number of rows: {common_ctx.obj.df.shape[0]}\n")
    display_df(get_null_columns(df=common_ctx.obj.df))


@cli.command()
@click.pass_context
@click.option("-c", "--column", type=str, help="Name of column to count the unique values for")
def value_counts(common_ctx, column):
    """
    Displays the unique values in a column
    """
    click.echo(f"\nFilename: {common_ctx.obj.filename + common_ctx.obj.file_extension} \nTotal number of rows: {common_ctx.obj.df.shape[0]}\n")
    display_df(get_value_counts(df=common_ctx.obj.df, column=column))


"""
FILTER AND QUERY
"""


@cli.command()
@click.pass_context
@click.option("-c", "--columns", type=str, help="Names of columns to show separated by commas")
@click.option("-s", "--sort-by", type=str, help="Name of column to sort by")
@click.argument("order", type=str, default="ASC", required=False)
@click.option("-save", "--save-to", type=str, help="Path to the destination file i.e. 'myfiles/data.csv'. The file extension determines output format")
def select(common_ctx, columns, sort_by, order, save_to):

    """
    Allows you to display subsets of columns and sort.
    """

    common_ctx.obj.df = filter_df(df=common_ctx.obj.df, columns=columns, sort_by=sort_by, order=order).copy()

    # we show result on screen if not save selected
    if save_to is None:

        display_df(df=common_ctx.obj.df)

    # if save selected, do not show result on screen, just write to file and confirm
    else:

        file_ext = get_file_extension(save_to)
        format = get_format_from_file_extension(file_extension=file_ext)

        success = output_to_file(df=common_ctx.obj.df,
                                 filepath=save_to,
                                 desired_format=format)

        if success:
            click.echo(f"successfully exported your selection result into {save_to}")
        else:
            click.echo(f"Ouch! Something went wrong. We could not export your selection result")


@cli.command()
@click.pass_context
@click.option("-q", "--query", type=str, help="SQL query you want to run against the file")
@click.option("-save", "--save-to", type=str, help="Path to the destination file i.e. 'myfiles/data.csv'. The file extension determines output format")
def query(common_ctx, query, save_to):

    """
    Allows you to query the file using SQL queries.
    """

    common_ctx.obj.df = filter_df_by_query(df=common_ctx.obj.df, query=query).copy()

    # we show result on screen if not save selected
    if save_to is None:
        click.echo(f'\nQUERY: "{query}"')
        click.echo(f"\nRESULT:\n")
        display_df(df=common_ctx.obj.df)

    # if save selected, do not show result on screen, just write to file and confirm
    else:

        file_ext = get_file_extension(save_to)
        format = get_format_from_file_extension(file_extension=file_ext)

        success = output_to_file(df=common_ctx.obj.df,
                                 filepath=save_to,
                                 desired_format=format)

        if success:
            click.echo(f"successfully exported your query result into {save_to}")

        else:
            click.echo(f"Ouch! Something went wrong. We could not export your query result")


"""
CHANGE THE FORMAT
"""


@cli.command()
@click.pass_context
@click.option("-to", "--format", type=str, help="Output format. Options: 'csv', 'excel' or 'parquet'")
@click.option("-D", "--delimiter", type=str, help="(optional) Only for CSV files. Delimiter if other than comma i.e. ';'. Must be a 1-character string.")
def convert(common_ctx, format, delimiter):

    """
    Allows you to convert to CSV, excel or parquet.
    """

    new_filepath = get_new_filepath(filepath=common_ctx.obj.filepath, desired_format=format)

    # if the new format is different from the original one
    if get_file_extension(filepath=new_filepath) != common_ctx.obj.file_extension:

        success = output_to_file(df=common_ctx.obj.df,
                                 filepath=new_filepath,
                                 desired_format=format,
                                 delimiter=delimiter)

        if success:
            delete_local_file(filepath=common_ctx.obj.filepath)
            click.echo(f"successfully converted {common_ctx.obj.filepath} to '{format}'")

        else:
            click.echo(f"Ouch! Something went wrong. We could not convert your file")

    else:
        click.echo("Ouch! The original formal of the file and the new format you selected are identical")


@cli.command()
@click.pass_context
@click.option("-to", "--new_delimiter", type=str, help="Output delimiter if other than comma i.e. ';'. Must be a 1-character string.")
def change_delimiter(common_ctx, new_delimiter):

    """
    Changes the delimiter of a CSV file.
    """

    if get_file_extension(filepath=common_ctx.obj.filepath) == '.csv':

        # create back up of original file
        os.system(f"cp {common_ctx.obj.filepath} temp")

        # attempt write op on file
        success = output_to_file(df=common_ctx.obj.df,
                                 filepath=common_ctx.obj.filepath,
                                 desired_format='csv',
                                 delimiter=new_delimiter)

        # if write op went through, delete back up
        if success:
            os.remove("temp")
            click.echo(f"successfully changed CSV delimiter of {common_ctx.obj.filepath} to '{new_delimiter}'")

        # else restore original from back up
        else:
            os.system(f"cp temp {common_ctx.obj.filepath}")
            os.remove("temp")
            click.echo(f"Ouch! Something went wrong, try with a different delimiter")


    else:
        click.echo("Ouch! You can only change delimiter of CSV files")