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

## Global parameters

Usage: csvcli [OPTIONS] FILEPATH COMMAND [ARGS]...

Arguments 

  - `FILEPATH` TEXT   Path to the file i.e. myfiles/data.csv. You might need to wrap it in "" if your filename contains parentheses and such.

Options:
  - `-d, --delimiter` TEXT  (optional) Only for CSV files. Delimiter if other than
                        comma i.e. ';'. Must be a 1-character string.
  
  - `--help `               Show this message and exit.


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

- `show`: Displays the contents of the CSV, excel or parquet file
  
  Example showing the contents of a CSV file with `,` as a delimiter.

  ```
  csvcli myfiles/data.csv show | less -S
  ```

  Example showing the contents of a CSV file with a delimiter other than commas. 
  In this case you must specify the delimiter using the `-d` option:

  ```
  csvcli -d '|' myfiles/csv_with_pipes.csv show | less -S
  ```

- `head`: Displays only the first rows of the file

  Options:
  - `-n, --rowcount` INTEGER  (optional) Number of rows to show.
  
  If you do not indicate any number, it returns the first 5 rows of the file:
  
  ```
  csvcli myfiles/data.csv head | less -S
  ```
  You can specify a custom number of rows to show using the `-n` option:
  ```
  csvcli myfiles/data.csv head -n 100 | less -S
  ```

- `columns`: Displays the column names and data types of the file
  
  ```
  csvcli myfiles/data.csv columns | less -S
  ```
  
- `describe`: Displays a table with summary statistics of the numerical columns
  
  ```
  csvcli myfiles/data.csv describe | less -S
  ```
- `null-counts`: Displays the counts of null values per column
  
  ```
  csvcli myfiles/data.csv null-counts | less -S
  ```
  
- `value-counts`: Displays the unique values in a column with their respective counts. 
  You must indicate a column using the `-c` option

  Options:
  - `-c, --column` TEXT  Name of column to count the unique values for
  
  Example 
  
  ```
  csvcli myfiles/data.csv value-counts -c "Region" | less -S
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

- `select`: Allows you to display only a subset of columns. 
  Also supports sorting by a given column.

   Options:
   - `-c, --columns` TEXT         Names of columns to show separated by commas
   - `-s, --sort-by` TEXT         Name of column to sort by
   - `-asc, --ascending` BOOLEAN  True for ascending and False for descending
   - `-save, --save-to` TEXT      Path to the destination file i.e.
                              'myfiles/data.csv'. The file extension determines
                              output format

    
   Example selecting columns from a CSV file:

   ```  
   csvcli myfiles/data.csv select -c "url, clicks, impressions" | less -S
   ```    
  
   Example selecting columns and sorting by one using the `-s` option. 
   You can add `ASC` for ascending order or `DESC` for descending order.
   The default is ascending:
   
   ```    
   csvcli myfiles/data.csv select -c "url, clicks, impressions" -s "clicks" DESC | less -S
   ```
    
   Example saving a selection result into an output file using the option `-save`:
    
   ``` 
   csvcli myfiles/data.csv select -c "region, count" -save "subset.csv"
   ```
    
- `query`: If you need more advanced filters and functions, the query command allows you to query the CSV, excel or parquet file using SQL queries as you would any regular SQL table. 
  You specify the query using the `-q` option and use the keyword `file` to refer to your file as a source table.
  
  Options:
  - `-q, --query` TEXT  SQL query you want to run against the file i.e. `SELECT * FROM file;`
  - `-save, --save-to` TEXT      Path to the destination file i.e.
                              'myfiles/data.csv'. The file extension determines
                              output format
  
  Example running a query on a CSV file:

  ```
  csvcli myfiles/data.csv query -q "SELECT Region,SUM(Units) FROM file GROUP BY Region;" | less -S
  ```
  
  Example saving a query result into an output file using the option `-save`:

  ```
  csvcli myfiles/data.csv query -q "SELECT Region,Units FROM file;" -save "query.csv"
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


- `convert`: Allows you to convert from and to CSV, excel and parquet in any combination. 
  Your original file will be overwritten.

 Options:
  - `-to, --format` TEXT    Output format. Options: 'csv', 'excel' or 'parquet'
  - `-D, --delimiter` TEXT  (optional) Only for CSV files. Delimiter if other than
                        comma i.e. ';'. Must be a 1-character string.
    
  Example converting a parquet file to CSV:

  ```
  csvcli myfiles/data.parquet convert -to "csv"
  ```

  Example converting an excel file to CSV with `|` as delimiter. using the `-D` option:

  ```
  csvcli myfiles/data.xlsx convert -to "csv" -D "|"
  ```


- `change-delimiter`: Changes the delimiter of a CSV file. 
  Your original file will be overwritten.

  Options:
    - `-D, --new_delimiter` TEXT  Output CSV delimiter i.e. ';'. Must be a
                            1-character string.
      
  Example changing the delimiter of a CSV file originally delimited by commas using the `-D` option:

  ```
  csvcli data.csv change-delimiter -D "|"
  ```
  
  Example changing the delimiter of a CSV file with a delimiter other than commas. 
  In this case you must also specify the old delimiter using the `-d` option:
  ```
  csvcli -d ";" data.csv change-delimiter -D "|"
  ```

## Note about the author

Ignacio Marin is a Data Analyst based in Munich, Germany.

More info on https://www.linkedin.com/in/ignaciomarinb/