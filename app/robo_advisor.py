# Robo Advisor Project OPIM 243

import csv
import json
import os

import requests
import pandas as pd
from dotenv import load_dotenv

import datetime

t = datetime.datetime.now()

load_dotenv()

# load_dotenv() #> loads contents of the .env file into the script's environment

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

if __name__ == "__main__":

    API_KEY = str(os.environ.get("ALPHAVANTAGE_API_KEY"))
    #print(API_KEY)

    while True:
        stock_ticker = input("Enter name of stock you want: ")
        if not stock_ticker.isalpha():
            print("Please make sure to enter name of stock price")
        else:
            data = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + stock_ticker + "&apikey=" + API_KEY)

            if "Error" in data.text:
                print("The stock you are looking for is not here")
            else:
                break

        # SHOUTOUT HIEP

    # API KEY request URL
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + stock_ticker + "&apikey=" + API_KEY


    response = requests.get(request_url)

    # print("RESPONSE STATUS: " + str(response.status_code))
    #print("RESPONSE TEXT: " + response.text)3. L

    parsed_response = json.loads(response.text)

    tsd = parsed_response["Time Series (Daily)"] #> 'dict'

    dates = list(tsd.keys())

    latest_day = "2019-02-20" 

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    latest_close = tsd[latest_day]["4. close"]

    # max of high prices
    high_prices = []
    low_prices = []
    close_prices = []

    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)

    # print(parsed_response["Time Series (Daily)"]["2019-02-19"]["4. close"])

    for date in dates:
        close_price = tsd[date]["4. close"]
        close_prices.append(float(close_price))

    mean_close = sum(close_prices)/len(close_prices)

    # PUTS THE DATA INTO A CSV FILE

    # output = pd.DataFrame(
    #     {
    #         "Time":t, "Mean Close":mean_close, "High": recent_high, "Low":recent_low, "Close":close_price,
    #     }
    # )

    # # deletes a file if it is named in the same way (the data would essentially be the same)

    # file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    # # https://stackoverflow.com/questions/9271464/what-does-the-file-variable-mean-do

    # # csv_headers = ["timestamp", "open", "high", "low", "close"]

    # # with(open(file_path,"w")) as csv_file:
    #     # writer_variable = csv.DictWriter(csv_file, fieldnames=csv_headers)
    #     # writer_variable.writeheader()
    #     # for date in dates:
    #         #dayprice = latest_day[date]
    #         writer_variable.writerow({
    #             "timestamp": date,
    #             "open": dayprice["1. open"],
    #             "high": dayprice["2. high"],
    #             "low": dayprice["3. low"],
    #             "close": dayprice["4. close"],
    #         })

    # # THANK YOU TO @IDEENAK and @GEORGEBRENNAN FOR THE HELP, THIS WAS CHALLENGING FOR ME AND HE WALKED ME THROUGH THE PROCESS

    print("--------------------------------")
    print("SELECTED SYMBOL: " + stock_ticker)
    print("--------------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUESTED AT: " + (t.strftime("%I:%M %p") + " ON " + (t.strftime("%Y-%m-%d"))))
    print(f"LAST REFRESHED: {last_refreshed}")
    print("--------------------------------")
    print(f"LATEST CLOSING PRICE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH PRICE: {to_usd(float(recent_high))}")
    print(f"RECENT LOW PRICE: {to_usd(float(recent_low))}")
    print(f"RUNNING 15 DAY AVG: {to_usd(float(mean_close))}")
    print("--------------------------------")

    if float(mean_close)>float(latest_close): 
        print("RECOMMENDATION: BUY")
        print ("We should buy this stock because its latest closing price is lower than its running 15-day average")
    else:
        print("RECOMMENDATION: SELL")
        print ("We should sell this stock because its latest closing price is higher than its running 15-day average")

    print("--------------------------------")
    print("HAPPY INVESTING") 
    print("--------------------------------")

