# Crypto-Historical-Prices
An ETL project that compiles historical cryptocurrency prices from online sources into one SQL database

## Introduction
This project enables anyone to get historical and up-to-date price information at the 1-minute level of granularity for the two largest cryptocurrency projects at the moment, Bitcoin and Ethereum. 

The Bitcoin data ranges from approximately December 2014 through this month (August 2020), and can be quickly and easily updated to include more recent data. 

The Ethereum data ranges from the re-release of Ethereum (when it split from Ethereum Classic via a major fork because of coin theft) around May 2016 through this month (August 2020) and can be updated easily using a Jupyter notebook at any time using this repository.

## Extract Data

The foundation of the data used in this project was pulled from kaggle.com, specifically from [here](https://www.kaggle.com/mczielinski/bitcoin-historical-data) for Bitcoin and [here](https://www.kaggle.com/prasoonkottarathil/ethereum-historical-dataset) for Ethereum. The initial data provided by these sources determined the earliest data points for this project, for reasons to be explained shortly. The 1-minute time interval was chosen because it was the smallest level of granularity, and the other data sets for hourly or daily prices could be closely replicated using this information. 

The Coinbase Pro "candles" API was used for gathering the more recent data (from January 2019 to August 2020 for Bitcoin and from April 2020 to August 2020 for Ethereum), and is used by to update the csvs and database to maintain consistency. The Bitcoin  data was originally drawn from Coinbase, as well as other exchanges, but the Coinbase API was free-to-use and works fine - see it [here](https://docs.pro.coinbase.com/#get-historic-rates). Unfortunately, the Coinbase API did not return historical prices at the 1-minute granularity level before the start dates for the Bitcoin or Ethereum data sets, so that data is not available in this project at this time - there may be a way to get more historical data at some point, especially using another exchange and possibly by paying to get an API key, so that will hopefully be added when/if possible.

## Transform Data 


## Load Data



## Update Data