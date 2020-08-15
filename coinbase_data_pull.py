import datetime as dt
import time
import pandas as pd
import requests

#setup basic API call function

#get the last time as a datetime object


def getLastTime(df):
    row = df.tail(1)
    timestamp = row["Unix Timestamp"]
    last_time = dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc)
    return last_time

#perform an api call - returns an array of arrays
#given the symbol as well, note that it is different for different currencies


def getData(last_time, curr_time, sym):
    time_diff = curr_time-last_time
    #gets about 5 hours per response, if the current time is more than 5 hours from the last time
    if(time_diff.total_seconds() >= ((4*60+59)*60)):
        new_time = last_time+dt.timedelta(hours=4, minutes=59)
        gran = 60
        start_time = last_time.isoformat().replace("+00:00", "")
        end_time = (new_time).isoformat().replace("+00:00", "")

        url = f"https://api.pro.coinbase.com/products/{sym}/candles?granularity={gran}&start={start_time}&end={end_time}"
        output = requests.get(url).json()
    #gets less than 5 hours data in response, if current time is less than 5 hours from the last time examined
    else:
        new_time = curr_time
        gran = 60
        start_time = last_time.isoformat().replace("+00:00", "")
        end_time = (curr_time).isoformat().replace("+00:00", "")

        url = f"https://api.pro.coinbase.com/products/{sym}/candles?granularity={gran}&start={start_time}&end={end_time}"
        output = requests.get(url).json()

    #implement a "wait" period to ensure that the API calls do not reach the rate limit
    #max requests -> 1 per second for the candles API as of 8/13/20
    time.sleep(2)
    return new_time, output

#put it all together in a function to repeatedly call the API until data is up to date
#must have a "Symbol" column with a valid coin identifier for the coinbase API (e.g. "BTC-USD" or "ETH-USD")
#add a time limit so that the final time is less than a year from the last time
#to break up data updates into smaller, ~hour long chunks


def get_current_data(df):
    orig_df_end_time = getLastTime(df)
    last_time = orig_df_end_time
    curr_time = dt.datetime.now(tz=dt.timezone.utc)
    results = []
    symbol = df["Symbol"].iloc[0]

    while((curr_time-last_time).total_seconds() >= 60 and last_time < (orig_df_end_time + dt.timedelta(days=365))):
        print(last_time.isoformat())
        curr_time = dt.datetime.now(tz=dt.timezone.utc)
        #add try/except loop to add robustness to API calls
        try:
            last_time, result = getData(last_time, curr_time, symbol)
        except:
            #case where data is not availble or there is an error in the request
            #so have an empty array as a dummy response
            print("ERROR - THERE IS NOT DATA RESPONSE")
            result = []
        results.append(result)

    return results

#get the raw API results returned from the 'get_current_data' function
def convert_results_to_df(output):
    #deconstruct the arrays
    data = []
    for response in output:
        if (not isinstance(response[0], int)):
            for item in response:
                data.append(item)

    print(len(data))

    api_call_df = pd.DataFrame(data, columns=['Unix Timestamp', 'Low', 'High', 'Open', 'Close',
                                            'Volume'])
    return api_call_df


#automates some of the cleaning needed from the initial df produced by 'convert_results_to_df'
#returns the new, cleaned data from the Coinbase API!
def clean_results_df(new_df, old_df):
    new_df["Date"] = new_df["Unix Timestamp"].apply(
        lambda x: dt.datetime.fromtimestamp(x, tz=dt.timezone.utc))

    new_df = new_df.sort_values(by="Unix Timestamp")
    new_df["Symbol"] = old_df["Symbol"]
    new_df = new_df.reset_index(drop=True)

    new_df = new_df.drop(0)

    new_df = remove_duplicate_times(new_df)

    return new_df


def remove_duplicate_times(df):
    check = df["Unix Timestamp"]


    condition = check.value_counts().max()
    # print("Max number of duplicates/repeated timestamp values: ", condition)

    #if true, there are some duplicates that need to be removed
    if(condition > 1):
        df.drop_duplicates(subset="Unix Timestamp", inplace=True)
        # print("This should be 1 if there were duplicates and all duplicates were removed",
        #     final_df["Unix Timestamp"].value_counts().max())

    return df