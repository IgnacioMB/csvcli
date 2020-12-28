# csvcli 0.0.1 (WIP)
## Description 
A simple command-line interface to work with CSV, excel and parquet files. You can use it to:
- navigate through the contents of your tabular data fast and with a human-friendly format directly on the shell
- quickly see which columns, data-types are inside
- select subsets of the tabular data and even run SQL queries on it

## Common parameters

These options are common to all commands

- `-f, --filepath` TEXT   Path to the file i.e.
                        `~/Downloads/super_important_data.csv`. 
  
- `-d, --delimiter` TEXT  Delimiter of the CSV file i.e. `;`. Must be a
                        1-character string. (optional, default ',')
  
- `--help`                Show the help message.


## Enhanced navigation with `less`

It is strongly encouraged to pipe the output of any command of `csvcli` to `less -S`. 
This will ensure that you can: 
- Visualize correctly the contents of the entire file regardless of its dimensions
  
- Navigate through the file using the arrow keys to scroll left/right and up/down

- Search for string patterns using `/pattern`
  - While in search use `n` go to the next line of the file containing the pattern
  - While in search use `N` go to the previous line of the file containing the pattern
  
- Quickly go to the beginning of the file using `g`
- Quickly go to the end of the file using `G`

For all these reasons all the examples provided here will include piping to `less -S`.

Full documentation on less: https://man7.org/linux/man-pages/man1/less.1.html
  
    

## Currently implemented commands

- show: displays the contents of the CSV, excel or parquet file
  
  Example showing the contents of a CSV file with `,` as a delimiter:

  ```
  csvcli "/Users/ignacio/Downloads/csv_with_commas.csv" show | less -S
  ```

  Example showing the contents of a CSV file with a delimiter other than commas. In this case you must specify the delimiter using the `-d` option:

  ```
  csvcli "/Users/ignacio/Downloads/csv_with_pipes.csv" -d '|' show | less -S
  ```

- head: displays only the first n rows of the CSV file (default 5 rows)

  Options:
  - `-n, --rowcount` INTEGER  Number of rows to show (optional)
  
  Example showing only the first 5 rows of the file:
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" head | less -S
  ```
  Example showing a custom number of rows. In this case you must specify the delimiter using the `-n` option:
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" head -n 100 | less -S
  ```

- columns: displays the column names and data types of the file
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" columns | less -S
  ```

- select: allows you to display only a subset of columns. Also supports sorting by a given column.

  Options:
  - `-c, --columns` TEXT         Names of columns to show separated by commas
  - `-s, --sort_by` TEXT         Name of column to order by (optional)
  - `-asc, --ascending` BOOLEAN  bool True for ascending and False for descending (optional)
  
  Example selecting 3 given columns from a CSV file:

  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" select -c "url, clicks, impressions" | less -S
  ```
  
  Example selecting 3 given columns and sorting by one. In this case you must specify the column you want to sort by using the `-s` option. The default ordering is descending:

  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" select -c "url, clicks, impressions" -s "clicks" | less -S
  ```
  
  Example selecting 3 given columns and sorting by one with ascending order. In this case you must specify that you want ascending order using the `-asc` option with a value of `True`:

  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" select -c "url, clicks, impressions" -s "clicks" -asc True | less -S
  ```
  
- query: allows you to query the CSV, excel or parquet file using SQL queries as you would any regular SQL table. You specify the query using the `-q` option and use the keyword `file` to refer to your file as a source table.
  
  Options:
  - `-q, --query` TEXT  SQL query you want to run against the file i.e. `SELECT * FROM file;`

  Example selecting all the rows and columns from a CSV file:

  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" query -q "SELECT * FROM file;" | less -S
  ```
  
  Example selecting a subset of rows from a CSV file:

  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" query -q "SELECT Region,Units FROM file;" | less -S
  ```
  
  Example running a GROUP BY query on a CSV file:

  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" query -q "SELECT Region,SUM(Units) FROM file GROUP BY Region;" | less -S
  ```

- describe: displays a table with summary statistics of the numerical columns
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" describe | less -S
  ```
- null-counts: displays the counts of null values are per column
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" null-counts
  ```
- change-delimiter: changes the delimiter of the CSV file

  Options:
    - `-D, --new_delimiter` TEXT  Output CSV delimiter i.e. ';'. Must be a
                            1-character string.
      
  Example changing the delimiter of a CSV file separated by commas. You must indicate the desired new delimiter using the `-D` option:

  ```
  csvcli -f "/Users/ignacio/Downloads/file.csv" change-delimiter -D "|"
  ```
  Example changing the delimiter of a CSV file with a delimiter other than commas. In this case you must also specify the old delimiter using the `-d` option:
  ```
  csvcli -f "/Users/ignacio/Downloads/file.csv" -d ";" change-delimiter -D "|"
  ```

  In both cases you will get a message confirming the change, and your original file will be overwritten.