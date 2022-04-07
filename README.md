# GE2/1 Cooling Circuit Monitor
## Erick Yanes, Bandar Alsufyani, Stephen D. Butalla
### 2022/04/07

Software used to retrieve data from temperature and humidity sensors on the GE2/1 cooling circuit.

The script is executed from the command line:

`python3 ge21_cooler_monitor.py [options]`

Available options are:

`-p`, `--printData", Prints data to standard output

`-w`, `--write`, Writes data to a text file

`-g`, `--googleSheet`, Sends data to a Google Sheet (not yet implemented)
    
