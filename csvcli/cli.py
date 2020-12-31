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
@click.option("-f", "--filepath", type=str, help="Path to the file i.e. 'myfiles/data.csv'.")
@click.option("-d", "--delimiter", type=str, default=",", help="(optional) Only for CSV files. Delimiter if other than comma i.e. ';'. Must be a 1-character string.")
def cli(common_ctx, filepath, delimiter):
    """

    WELCOME to csvcli, a simple command-line interface to work with CSV, excel and parquet files.

    You can use it to:

    - Explore your data: navigate through the full contents of your tabular data fast and with a human-friendly format directly on the shell.
      Quickly see which columns, data-types are in the file and how many null values or unique values are per column.

    - Filter and query: select subsets of the tabular data, sort by a given column... Need more? Ok then just run SQL queries on it! In all cases you can save the output to a new file

    - Change the format: you can convert from and to CSV, excel and parquet in any combination. You can change the delimiter of your CSV file

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

    Example showing the contents of a CSV file with `,` as a delimiter.
    You indicate the file you want to open using the `-f` option:


        csvcli -f "csv_with_commas.csv" show | less -S


    Example showing the contents of a CSV file with a delimiter other than commas.
    In this case you must specify the delimiter using the `-d` option:


        csvcli -f "csv_with_pipes.csv" -d '|' show | less -S

    """

    display_df(df=common_ctx.obj.df)


@cli.command()
@click.pass_context
@click.option("-n", "--rowcount", type=int, default=5, help="(optional) Number of rows to show.")
def head(common_ctx, rowcount):
    """

    Displays only the first rows of the file.

    If you do not indicate any number, it returns the first 5 rows of the file:

        csvcli -f "csv_with_commas.csv" head | less -S

    You can specify a custom number of rows to show using the `-n` option:

        csvcli -f "csv_with_commas.csv" head -n 100 | less -S

    """
    common_ctx.obj.df = filter_df(df=common_ctx.obj.df, head=True, n=rowcount).copy()
    display_df(df=common_ctx.obj.df)


@cli.command()
@click.pass_context
def columns(common_ctx):
    """

    Displays the column names and data types of the file.


        csvcli -f "myfiles/data.csv" columns | less -S

    """
    display_df(get_dtypes(df=common_ctx.obj.df, pretty=True))


@cli.command()
@click.pass_context
def describe(common_ctx):
    """

    Displays a table with summary statistics of the numerical columns.


        csvcli -f "myfiles/data.csv" describe | less -S

    """

    display_df(get_summary_stats(df=common_ctx.obj.df))


@cli.command()
@click.pass_context
def null_counts(common_ctx):
    """

    Displays the counts of null values per column.


        csvcli -f "myfiles/data.csv" null-counts | less -S

    """
    display_df(get_null_columns(df=common_ctx.obj.df))


@cli.command()
@click.pass_context
@click.option("-c", "--column", type=str, help="Name of column to count the unique values for")
def value_counts(common_ctx, column):
    """

    Displays the unique values in a column with their respective counts.
    You must indicate a column using the `-c` option.

    Example

        csvcli -f "myfiles/data.csv" value-counts -c "Region" | less -S

    """
    display_df(get_value_counts(df=common_ctx.obj.df, column=column))


"""
FILTER AND QUERY
"""


@cli.command()
@click.pass_context
@click.option("-c", "--columns", type=str, help="Names of columns to show separated by commas")
@click.option("-s", "--sort-by", type=str, help="Name of column to sort by")
@click.option("-asc", "--ascending", type=bool, help="True for ascending and False for descending")
@click.option("-save", "--save-to", type=str, help="Path to the destination file i.e. 'myfiles/data.csv'. The file extension determines output format")
def select(common_ctx, columns, sort_by, ascending, save_to):

    """

    Allows you to display only a subset of columns. Also supports sorting by a given column.

    Example selecting columns from a CSV file:


        csvcli -f "myfiles/data.csv" select -c "url, clicks, impressions" | less -S


    Example selecting columns and sorting by one using the `-s` option. The default order is descending:


        csvcli -f "myfiles/data.csv" select -c "url, clicks, impressions" -s "clicks" | less -S


    Example selecting columns and sorting by one with ascending order using the `-asc` option:


        csvcli -f "myfiles/data.csv" select -c "url, clicks, impressions" -s "clicks" -asc True | less -S


    Example saving a selection result into an output file using the option `-save`:


        csvcli -f "myfiles/data.csv" select -c "region, count" -save "subset.csv"

    """

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

        click.echo(f"successfully wrote select result into {save_to}")


@cli.command()
@click.pass_context
@click.option("-q", "--query", type=str, help="SQL query you want to run against the file")
@click.option("-save", "--save-to", type=str, help="Path to the destination file i.e. 'myfiles/data.csv'. The file extension determines output format")
def query(common_ctx, query, save_to):

    """

    Allows you to query the CSV, excel or parquet file using SQL queries as you would any regular SQL table.
    You specify the query using the `-q` option and use the keyword `file` to refer to your file as a source table.

    Example running a query on a CSV file:

        csvcli -f "myfiles/data.csv" query -q "SELECT Region,SUM(Units) FROM file GROUP BY Region;" | less -S


    Example saving a query result into an output file using the option `-save`:

        csvcli -f "myfiles/data.csv" query -q "SELECT Region,Units FROM file;" -save "query.csv"


    """

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

        click.echo(f"successfully wrote query result into {save_to}")


"""
CHANGE THE FORMAT
"""


@cli.command()
@click.pass_context
@click.option("-to", "--format", type=str, help="Output format. Options: 'csv', 'excel' or 'parquet'")
@click.option("-D", "--delimiter", type=str, help="(optional) Only for CSV files. Delimiter if other than comma i.e. ';'. Must be a 1-character string.")
def convert(common_ctx, format, delimiter):

    """

    Allows you to convert from and to CSV, excel and parquet in any combination. Your original file will be overwritten.

    Example converting a parquet file to CSV:

        csvcli -f "myfiles/data.parquet" convert -to "csv"


    Example converting an excel file to CSV with `|` as delimiter. using the `-D` option:


        csvcli -f "myfiles/data.xlsx" convert -to "csv" -D "|"

    """

    new_filepath = get_new_filepath(filepath=common_ctx.obj.filepath, desired_format=format)

    # if the new format is different from the original one
    if get_file_extension(filepath=new_filepath) != common_ctx.obj.file_extension:

        output_to_file(df=common_ctx.obj.df,
                       filepath=new_filepath,
                       desired_format=format,
                       delimiter=delimiter)

        delete_local_file(filepath=common_ctx.obj.filepath)

        click.echo(f"successfully converted {common_ctx.obj.filepath} to '{format}'")

    else:
        click.echo("Ouch! The original formal of the file and the new format you selected are identical")


@cli.command()
@click.pass_context
@click.option("-D", "--new_delimiter", type=str, help="Output delimiter if other than comma i.e. ';'. Must be a 1-character string.")
def change_delimiter(common_ctx, new_delimiter):

    """

    Changes the delimiter of a CSV file. Your original file will be overwritten.

    Example changing the delimiter of a CSV file originally delimited by commas using the `-D` option:

        csvcli -f "data.csv" change-delimiter -D "|"

    Example changing the delimiter of a CSV file with a delimiter other than commas. In this case you must also specify the old delimiter using the `-d` option:

        csvcli -f "/Users/ignacio/Downloads/file.csv" -d ";" change-delimiter -D "|"

    """

    if get_file_extension(filepath=common_ctx.obj.filepath) == '.csv':
        output_to_file(df=common_ctx.obj.df,
                       filepath=common_ctx.obj.filepath,
                       desired_format='csv',
                       delimiter=new_delimiter)

        click.echo(f"successfully changed CSV delimiter of {common_ctx.obj.filepath} to '{new_delimiter}'")

    else:
        click.echo("Ouch! You can only change delimiter of CSV files")