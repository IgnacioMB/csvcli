```
                                          ___           
                                         /\_ \    __    
      ___    ____  __  __             ___\//\ \  /\_\   
     /'___\ /',__\/\ \/\ \  _______  /'___\\ \ \ \/\ \  
    /\ \__//\__, `\ \ \_/ |/\______\/\ \__/ \_\ \_\ \ \ 
    \ \____\/\____/\ \___/ \/______/\ \____\/\____\\ \_\
     \/____/\/___/  \/__/            \/____/\/____/ \/_/
 
```
## Description 
A simple command-line interface to work with CSV, excel and parquet files. You can use it to:
- Explore your data: 
  - navigate through the full contents of your tabular data fast and with a human-friendly format directly on the shell
  - quickly see which columns, data-types are in the file and how many null values or unique values are per column
  
- Filter and query: 
  - select subsets of the tabular data
  - sort by a given column
  - Need more? Ok then just run SQL queries on it!
  - In all cases you can save the output to a new file
  
- Change the format:
  - You can convert from and to CSV, excel and parquet in any combination
  - You can change the delimiter of your CSV file

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
  
    

## Available commands

```
                     ___                          
                    /\_ \                         
   __   __  _  _____\//\ \     ___   _ __    __   
 /'__`\/\ \/'\/\ '__`\\ \ \   / __`\/\`'__\/'__`\ 
/\  __/\/>  </\ \ \L\ \\_\ \_/\ \L\ \ \ \//\  __/ 
\ \____\/\_/\_\\ \ ,__//\____\ \____/\ \_\\ \____\
 \/____/\//\/_/ \ \ \/ \/____/\/___/  \/_/ \/____/
                 \ \_\                            
                  \/_/                            
                  
                  
               __  __    ___   __  __  _ __  
              /\ \/\ \  / __`\/\ \/\ \/\`'__\
              \ \ \_\ \/\ \L\ \ \ \_\ \ \ \/ 
               \/`____ \ \____/\ \____/\ \_\ 
                `/___/> \/___/  \/___/  \/_/ 
                   /\___/                    
                   \/__/    
     

                          __            __               
                         /\ \          /\ \__            
                         \_\ \     __  \ \ ,_\    __     
                         /'_` \  /'__`\ \ \ \/  /'__`\   
                        /\ \L\ \/\ \L\.\_\ \ \_/\ \L\.\_ 
                        \ \___,_\ \__/.\_\\ \__\ \__/.\_\
                         \/__,_ /\/__/\/_/ \/__/\/__/\/_/                 

```

These commands allow you to quickly get a sense of what the contents of the file look like.

- `show`: displays the contents of the CSV, excel or parquet file
  
  Example showing the contents of a CSV file with `,` as a delimiter:

  ```
  csvcli "/Users/ignacio/Downloads/csv_with_commas.csv" show | less -S
  ```

  Example showing the contents of a CSV file with a delimiter other than commas. In this case you must specify the delimiter using the `-d` option:

  ```
  csvcli "/Users/ignacio/Downloads/csv_with_pipes.csv" -d '|' show | less -S
  ```

- `head`: displays only the first n rows of the CSV file (default 5 rows)

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

- `columns`: displays the column names and data types of the file
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" columns | less -S
  ```
  
- `describe`: displays a table with summary statistics of the numerical columns
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" describe | less -S
  ```
- `null-counts`: displays the counts of null values per column
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" null-counts | less -S
  ```
  
- `value-counts`: displays the unique values in a column with their respective counts. You must indicate a column using the `-c` option

  Options:
  - `-c, --column` TEXT  Name of column to count the unique values for
  
  Example 
  
  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" value-counts -c "Region" | less -S
  ```

  
```

   ___      ___    __                   
 /'___\ __ /\_ \  /\ \__                
/\ \__//\_\\//\ \ \ \ ,_\    __   _ __  
\ \ ,__\/\ \ \ \ \ \ \ \/  /'__`\/\`'__\
 \ \ \_/\ \ \ \_\ \_\ \ \_/\  __/\ \ \/ 
  \ \_\  \ \_\/\____\\ \__\ \____\\ \_\ 
   \/_/   \/_/\/____/ \/__/\/____/ \/_/ 
   
   
                          ____      
                        /|  _ \     
                        |/\   |     
                         \// __`\/\ 
                         /|  \L>  <_
                         | \_____/\/
                          \/____/\/ 
                        
                        
                         __   __  __     __   _ __   __  __    
                       /'__`\/\ \/\ \  /'__`\/\`'__\/\ \/\ \   
                      /\ \L\ \ \ \_\ \/\  __/\ \ \/ \ \ \_\ \  
                      \ \___, \ \____/\ \____\\ \_\  \/`____ \ 
                       \/___/\ \/___/  \/____/ \/_/   `/___/> \
                            \ \_\                        /\___/
                             \/_/                        \/__/ 


```

- `select`: allows you to display only a subset of columns. Also supports sorting by a given column.

  Options:
  - `-c, --columns` TEXT         Names of columns to show separated by commas
  - `-s, --sort_by` TEXT         Name of column to order by (optional)
  - `-asc, --ascending` BOOLEAN  bool True for ascending and False for descending (optional)
  - `-save, --save_to TEXT`      Destination path i.e. '~/Downloads/my_query.csv'.
                             The file extension of your destination path
                             determines output format
    
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
  
  Example saving a selection result into an output file. In this case you need to indicate that you want to save and where by using the option `-save`:

  ```
  csvcli -f "impressions.csv" select -c "region_id, count" -save "subset.csv"
  ```
  
- `query`: If you need more advanced filters and functions, the query command allows you to query the CSV, excel or parquet file using SQL queries as you would any regular SQL table. You specify the query using the `-q` option and use the keyword `file` to refer to your file as a source table.
  
  Options:
  - `-q, --query` TEXT  SQL query you want to run against the file i.e. `SELECT * FROM file;`
  - `-save, --save_to TEXT`      Destination path i.e. '~/Downloads/my_query.csv'.
                             The file extension of your destination path
                             determines output format

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
  
  Example saving a query result into an output file. In this case you need to indicate that you want to save and where by using the option `-save`:

  ```
  csvcli -f "/Users/ignacio/Downloads/csv_with_commas.csv" query -q "SELECT Region,Units FROM file;" -save "query.csv"
  ```

```
      __                                         
     /\ \                                        
  ___\ \ \___      __      ___      __      __   
 /'___\ \  _ `\  /'__`\  /' _ `\  /'_ `\  /'__`\ 
/\ \__/\ \ \ \ \/\ \L\.\_/\ \/\ \/\ \L\ \/\  __/ 
\ \____\\ \_\ \_\ \__/.\_\ \_\ \_\ \____ \ \____\
 \/____/ \/_/\/_/\/__/\/_/\/_/\/_/\/___L\ \/____/
                                    /\____/      
                                    \_/__/       
                                    
                                  
                   __    __                
                  /\ \__/\ \               
                  \ \ ,_\ \ \___      __   
                   \ \ \/\ \  _ `\  /'__`\ 
                    \ \ \_\ \ \ \ \/\  __/ 
                     \ \__\\ \_\ \_\ \____\
                      \/__/ \/_/\/_/\/____/
    
    
               ___                                   __      
             /'___\                                 /\ \__   
            /\ \__/  ___   _ __    ___ ___      __  \ \ ,_\  
            \ \ ,__\/ __`\/\`'__\/' __` __`\  /'__`\ \ \ \/  
             \ \ \_/\ \L\ \ \ \/ /\ \/\ \/\ \/\ \L\.\_\ \ \_ 
              \ \_\\ \____/\ \_\ \ \_\ \_\ \_\ \__/.\_\\ \__\
               \/_/ \/___/  \/_/  \/_/\/_/\/_/\/__/\/_/ \/__/

```


- `convert`: allows you to convert from and to CSV, excel and parquet in any combination

 Options:
  - `-to, --format` TEXT    Output format. Options: 'csv', 'excel' or 'parquet'
  - `-D, --delimiter` TEXT  Output CSV delimiter i.e. ';'. Must be a 1-character
                        string (only if you convert to csv and want other  than comma)
    
  Example converting a parquet file to CSV:

  ```
  csvcli -f "seo.parquet" convert -to "csv"
  ```

  Example converting an excel file to CSV with `|` as delimiter. As you wish a delimiter other than the default comma, you need to indicate it using the `-D` option:

  ```
  csvcli -f "impressions.xlsx" convert -to "csv" -D "|"
  ```


- `change-delimiter`: changes the delimiter of the CSV file

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

## Note about the author

Ignacio Marin is a Data Analyst based in Munich, Germany.

More info on https://www.linkedin.com/in/ignaciomarinb/