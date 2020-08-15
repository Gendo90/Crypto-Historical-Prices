# Crypto-Historical-Prices
An ETL project that compiles historical cryptocurrency prices from online sources into one SQL database

## Introduction
This project enables anyone to get historical and up-to-date price information at the 1-minute level of granularity for the two largest cryptocurrency projects at the moment, Bitcoin and Ethereum. 

The Bitcoin data ranges from approximately December 2014 through this month (August 2020), and can be quickly and easily updated to include more recent data. 

The Ethereum data ranges from the re-release of Ethereum (when it split from Ethereum Classic via a major fork because of coin theft) around May 2016 through this month (August 2020) and can be updated easily using a Jupyter notebook at any time using this repository.


## Extract Data

### Downloaded Files

The foundation of the data used in this project was pulled from kaggle.com, specifically from [here](https://www.kaggle.com/mczielinski/bitcoin-historical-data) for Bitcoin and [here](https://www.kaggle.com/prasoonkottarathil/ethereum-historical-dataset) for Ethereum. The initial data provided by these sources determined the earliest data points for this project, for reasons to be explained shortly. The 1-minute time interval was chosen because it was the smallest level of granularity, and the other data sets for hourly or daily prices could be closely replicated using this information. 

Two .csv files were used as the backbone of this project. The first, for Bitcoin, is named **bitstampUSD_1-min_data_2012-01-01_to_2020-04-22.csv**
and is available [here]() in this repository or from the link above.

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

Some examples of the transform process that involved cleaning and updating the data would include dropping null values, ensuring that the Unix timestamps are sorted and contain no duplicate values, and that the cryptocurrency symbol and date formats match the requirements of the Coinbase API. In fact, every time the csv data is read, the "Date" column (which is an aware datetime object) needs to be converted to the correct 
type. Converting this column automatically is one of the planned features of this project.

There is a combined "Extract and Transform" Jupyter notebook in this repository, but it is rough and will be refined when possible, likely when a new data set is introduced. There is no need to run this notebook, but anyone can look through it for to get some idea of the iterative data cleaning process involved with this sort of data.

## Load Data

### Create SQL Tables

The file [**create_tables.sql**](./create_tables.sql) should be loaded or copied into a PostgreSQL database editor, like pgAdmin. Once the code to create the 'bitcoin' and 'ethereum' tables is loaded, run the code to create those two tables. This must be completed **before** the next step, or it will not work.

The tables have the same structure but different values. The basic table columns are as follows:

`[unix_timestamp, entry_date, symbol, open_price, high_price, low_price, close_price, coin_volume]`

These column names were chosen as SQL-compatible names, because some of the original column names had spaces in them ("Unix Timestamp") and a lot of the others were important in the SQL language ("Date", "Open", "Close", etc.).

The tables have the following kinds of data types, corresponding to each column:

`[INT, TIMESTAMP WITH TIME ZONE, VARCHAR(10), DECIMAL, DECIMAL, DECIMAL, DECIMAL, DECIMAL]`

The tables have composite primary keys, which consists of the "unix_timestamp" and "symbol" columns because that combination should be unique for each table and across other tables - because different tables could have the same timestamp values but then they would have different symbols, and the timestamp values should be unique within a single table (no duplicate data) even if they all share the same symbol. This combination could therefore be helpful in identifying data in future tables that consist of combinations (or aggregations - basically any transformation) of the data from the raw coin price tables created here.


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

* Open [this notebook](./Update_Data.ipynb) and run once the data has been loaded into SQL to confirm that the .csv file and database information match for a specific cryptocurrency, and then scrape data from the Coinbase API to update the .csv file and database table for that specific cryptocurrency to the current time!
* Please note that **Update_Data.ipynb** should be the only notebook you run after the data has initially been loaded into the SQL database, as described above. None of the other notebooks should be touched after that point!
* Finally, the notebook only updates the data by one year maximum. So if you had a cryptocurrency with data from 2015 and it is now 2020, you may need to run the notebook about 5 times successively to get the most up-to-date data from 2020. This date limit was created to break the updates for long periods into chunks - scraping about a year of data takes about an hour on my laptop, so breaking the work into smaller segments makes the process more robust and reliable.