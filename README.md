# csvcli 0.0.1 (WIP)
## Description 
A simple command-line interface to work with CSV files

## Common parameters

These parameters are common to all commands

- `-f, --filepath` TEXT   Path to the CSV file i.e.
                        '~/Downloads/super_important_data.csv'. 
  
- `-d, --delimiter` TEXT  Delimiter of the CSV file i.e. ','. Must be a
                        1-character string.
  
- `--help`                Show the help message.

## Currently implemented commands

- show: displays the contents of the CSV file
  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," show
  ```
  It is strongly recommended to pipe the output to `less -S`. 
  This will allow to visualize correctly the contents of the entire CSV file regardless of its dimensions and to navigate through it using the arrow keys to scroll left and right. This applies also to the rest of commands.
    
  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," show | less -S
  ```
- head: displays only the first 5 rows of the CSV file
  
  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," head
  ```
- nhead: displays only the first n rows of the CSV file

  Parameters
  - `-n, --rowcount` INTEGER  Number of rows to show
  
  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," nhead 7
  ```

- cols: displays the column names and data types of the CSV file
  
  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," cols
  ```
- describe: displays a table with summary statistics
  
  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," describe
  ```
- nullcols: displays how many null values are per column
  
  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," nullcols
  ```
- change-delimiter: changes the delimiter of the CSV file

  Parameters:
    - `-D, --new_delimiter` TEXT  Output CSV delimiter i.e. ';'. Must be a
                            1-character string.

  ```
  csvcli -f "/Users/ignacio/Downloads/sc_converted.csv" -d "," change-delimiter -D "|"
  ```



