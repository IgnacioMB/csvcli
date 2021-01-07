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
A light-weight command-line tool to browse and query CSV, Excel and Apache Parquet files, regardless of their size. 
You can use it to:
- Explore your data: 
  - Navigate through the full contents of your tabular data fast and with a human-friendly format directly on the shell
  - Quickly see which columns, data-types are in the file and how many null values or unique values are per column
  - csvcli can handle and manipulate extremely large tabular data. There are no long loading times, regardless of the size of your file.
  
- Filter and query: 
  - Select subsets of the tabular data
  - Sort by a given column
  - Need more? Ok then just run SQL queries on it!
  - In all cases you can save the output to a new file
  
- Change the format:
  - You can convert from and to CSV, Excel and Apache Parquet in any combination
  - You can also change the delimiter of your CSV file
  
## Why?

Browsing and filtering large CSV files and Excel files in programs like Microsoft Excel or Pages can be slow and there are limitations to the amount of rows displayed.
Apache Parquet files cannot even be opened by these programs.
Additionally, working with the command-line can help you streamline your work and avoid distractions.
csvcli allows you to get insights from your data and run queries on them regardless of its size and format, directly from the command line.

  
## Python version
Built on and tested on python 3.7

## Installation
### Using Pip
```bash
  $ pip install csvcli
```
### Manual
```bash
  $ git clone https://github.com/IgnacioMB/csvcli.git
  $ cd csvcli
  $ python setup.py install
```

## Global parameters

Usage: csvcli [OPTIONS] FILEPATH COMMAND [ARGS]...

Arguments 

  - `FILEPATH` TEXT   Path to the file i.e. myfiles/data.csv. You might need to wrap it in "" if your filename contains parentheses and such.

Options:
  - `-d, --delimiter` TEXT  (optional) Only for CSV files. If you want to override the automatic guess. Must be a 1-character string.
  
  - `--help `               Show this message and exit.
  
    

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

- `show`: Displays the full contents of the CSV, Excel or Apache Parquet file. 
  
  Navigation:
  - Use the arrow keys to scroll through the rows or columns
  - Press 'z' to go to the end of the file
  - Press 'a' to go the beginning of the file
  - Press 'q' to quit
  
  Example showing the contents of a CSV file.

  ```
  csvcli myfiles/data.csv show
  ```

  While working with CSV files, csvcli will try to guess the delimiter of your CSV files for you.
  If you are not happy with the guess, you can always specify the delimiter using the `-d` option:

  ```
  csvcli -d '|' myfiles/csv_with_pipes.csv show
  ```
  
  

- `head`: Displays only the first rows of the file
  
  If you do not indicate any number, it returns the first 5 rows of the file:
  
  ```
  csvcli myfiles/data.csv head
  ```
  
  You can also specify a custom number of rows to show:
  ```
  csvcli myfiles/data.csv head 100
  ```

- `columns`: Displays the column names and data types
  
  ```
  csvcli myfiles/data.csv columns
  ```
  
- `describe`: Displays a table with summary statistics of the numerical columns
  
  ```
  csvcli myfiles/data.csv describe
  ```
- `null-counts`: Displays the counts of null values per column
  
  ```
  csvcli myfiles/data.csv null-counts
  ```
  
- `value-counts`: Displays the unique values in a column with their respective counts. 
  You must indicate a column using the `-c` option

  Options:
  - `-c, --column` TEXT  Name of column to count the unique values for
  
  Example 
  
  ```
  csvcli myfiles/data.csv value-counts -c "Region"
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
  
   Arguments:
   - `ASC` TEXT  For ascending sorting
  - `DESC` TEXT  For descending sorting

   Options:
   - `-c, --columns` TEXT         Names of selected columns to show separated by commas
   - `-s, --sort-by` TEXT         Name of column to sort by
   - `-save, --save-to` TEXT      Path to the destination file i.e.
                              'myfiles/data.csv'. The file extension determines
                              output format

    
   Example selecting columns from a CSV file:

   ```  
   csvcli myfiles/data.csv select -c "url, clicks, impressions"
   ```    
  
   Example selecting columns and sorting by one using the `-s` option. 
   You can add `ASC` for ascending order or `DESC` for descending order.
   The default is ascending:
   
   ```    
   csvcli myfiles/data.csv select -c "url, clicks, impressions" -s "clicks" DESC
   ```
    
   Example saving a selection result into an output file using the option `-save`:
    
   ``` 
   csvcli myfiles/data.csv select -c "region, count" -save subset.csv
   ```
    
- `query`: If you need more advanced filters and functions, the query command allows you to query the CSV, Excel or Apache Parquet file using SQL queries as you would any regular SQL table. 
  You specify the query using the `-q` option and use the keyword `file` to refer to your file as a source table. Uses [SQLite](https://www.sqlite.org/lang.html) syntax.
  
  Options:
  - `-q, --query` TEXT  SQL query you want to run against the file i.e. `SELECT * FROM file;`
  - `-save, --save-to` TEXT      Path to the destination file i.e.
                              'myfiles/data.csv'. The file extension determines
                              output format
  
  Example running a query on a CSV file:

  ```
  csvcli myfiles/data.csv query -q "SELECT Region,SUM(Units) FROM file GROUP BY Region;"
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


- `convert`: Allows you to convert from and to CSV, Excel and Apache Parquet in any combination. 
  Your original file will be overwritten.

 Options:
  - `-to, --format` TEXT    Output format. Options: `'csv', 'excel' or 'parquet'`
  - `-D, --delimiter` TEXT  (optional) Only for CSV files. Delimiter if other than
                        comma i.e. ';'. Must be a 1-character string.
    
  Example converting a parquet file to CSV:

  ```
  csvcli myfiles/data.parquet convert -to csv
  ```

  Example converting an Excel file to CSV with `|` as delimiter. using the `-D` option:

  ```
  csvcli myfiles/data.xlsx convert -to "csv" -D "|"
  ```


- `change-delimiter`: Changes the delimiter of a CSV file. 
  Your original file will be overwritten.

  Options:
    - `-to, --new-delimiter` TEXT  Output CSV delimiter i.e. ';'. Must be a
                            1-character string.
  
  Example changing the delimiter of a CSV file from ';' to '|':
  
  ```
  csvcli -d ";" data.csv change-delimiter -to "|"
  ```

## Note about the author

Ignacio Marin is a Data Analyst based in Munich, Germany.

More info on https://www.linkedin.com/in/ignaciomarinb/