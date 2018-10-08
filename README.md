# CRYPTO DATA

This script is aimed to get cryptocurrency data from Binance exange. The code will retrieve close prices for currencies greather than 1e9 market cap from the days selected and within the frequency chosen. 

### Dependencies
* pandas
* numpy
* Beautifilsoup
* requests
* time
* json
* python-binance


### Running the script
The script to run is called 'main.py'. This cript need 3 parameters:
* --I: initial_date. The initial date that is going to start the data retrieving
* --F: final_date. The end date to retrieve the data
* --Freq: freq. Frequency of the data stored. The list of supported frequencies are: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h','1d','3d', '1w', '1M']

Eg of the running script:
```
$ python main.py --I '2017-06-01' --F '2018-10-06' --Freq '1h'
```
