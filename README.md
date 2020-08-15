# Crypto-Historical-Prices
An ETL project that compiles historical cryptocurrency prices from online sources into one SQL database

## Introduction
This project enables anyone to get historical and up-to-date price information at the 1-minute level of granularity for the two largest cryptocurrency projects at the moment, Bitcoin and Ethereum. 

The Bitcoin data ranges from approximately December 2014 through this month (August 2020), and can be quickly and easily updated to include more recent data. 

The Ethereum data ranges from the re-release of Ethereum (when it split from Ethereum Classic via a major fork because of coin theft) around May 2016 through this month (August 2020) and can be updated easily using a Jupyter notebook at any time using this repository.


## Extract Data

### Downloaded Files

The foundation of the data used in this project was pulled from kaggle.com, specifically from [here](https://www.kaggle.com/mczielinski/bitcoin-historical-data) for Bitcoin and [here](https://www.kaggle.com/prasoonkottarathil/ethereum-historical-dataset) for Ethereum. The initial data provided by these sources determined the earliest data points for this project, for reasons to be explained shortly. The 1-minute time interval was chosen because it was the smallest level of granularity, and the other data sets for hourly or daily prices could be closely replicated using this information. 

### API to Update Data

The Coinbase Pro "candles" API was used for gathering the more recent data (from January 2019 to August 2020 for Bitcoin and from April 2020 to August 2020 for Ethereum), and is used by to update the csvs and database to maintain consistency. The Bitcoin  data was originally drawn from Coinbase, as well as other exchanges, but the Coinbase API was free-to-use and works fine - see it [here](https://docs.pro.coinbase.com/#get-historic-rates). Unfortunately, the Coinbase API did not return historical prices at the 1-minute granularity level before the start dates for the Bitcoin or Ethereum data sets, so that data is not available in this project at this time - there may be a way to get more historical data at some point, especially using another exchange and possibly by paying to get an API key, so that will hopefully be added when/if possible.

## Transform Data 

The data had to be transformed from its original state into workable, clear
columns for human usage. Both datasets use the same columns in the .csv's from this project, and this standardized format is scalable if more cryptocurrencies are added at a later date. The column headers in the .csv 
files are:

`["Unix Timestamp", "Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]`

are measured in the following units: 

`[Epoch Time, YYYY-MM-DD HH:MM:SS+GMT, 'Coin Code'-'Fiat Currency Code', Fiat Currency, Fiat Currency, Fiat Currency, Fiat Currency, # of Coins]`

and have the Python data types: 

`[int64, datetime64[ns, UTC], object, float64, float64, float64, float64, float64]`

respectively.

The data cleaning process is beyond the scope of this README - needless to say, it is usually 80% of the work on any given data science project, and this was no exception! Any new data sources, for more cryptocurrencies or older Bitcoin or Ethereum prices, would need to be carefully, manually cleaned and standardized to match the csv's included in this repo already. 

There is a combined "Extract and Transform" Jupyter notebook in this repository, but it is rough and will be refined when possible, likely when a new data set is introduced. There is no need to run this notebook, but anyone can look through it for to get some idea of the iterative data cleaning process involved with this sort of data.

## Load Data

### Create SQL Tables

The file [**create_tables.sql**](./create_tables.sql) should be loaded or copied into a PostgreSQL database editor, like pgAdmin. Once the code to create the 'bitcoin' and 'ethereum' tables is loaded, run the code to create those two tables. This must be completed **before** the next step, or it will not work.


### Load Cryptocurrencies into SQL

* Create a config file named `config.py` in the main repo directory - [here](./)  - in order to load your specific username and password for PostgreSQL. The file should contain only two lines, that look like: 

        user = 'USERNAME'
        pw = 'PASSWORD'
    where the `USERNAME` is the username for your PostgreSQL database, and `PASSWORD` is the password for the database.

* You are now ready to run [this notebook](./ETH\ \&\ BTC\ Load\ Into\ SQL.ipynb) and load the .csv data into your database!
* Follow the instructions provided in the "ETH & BTC Load Into SQL.ipynb" notebook listed above. Remember to check your connection string to connect on the correct port to the correct database! There should be printed feedback that you have loaded first the Ethereum, and then the Bitcoin data correctly.
* There will now be two tables in your database - 
    * bitcoin
    * ethereum

    More may be added later!

## Update Data