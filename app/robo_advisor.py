# goal: print the latest closing price

import csv
import json
import os

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# load_dotenv() #> loads contents of the .env file into the script's environment

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
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

# "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=demo"
#request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey=" + API_KEY
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + stock_ticker + "&apikey=" + API_KEY
print(request_url)

response = requests.get(request_url)

print("RESPONSE STATUS: " + str(response.status_code))
#print("RESPONSE TEXT: " + response.text)3. L

parsed_response = json.loads(response.text)

tsd = parsed_response["Time Series (Daily)"] #> 'dict'

dates = list(tsd.keys())

latest_day = "2019-02-20" # TODO: make dynamic

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
latest_close = tsd[latest_day]["4. close"]

# max of high prices
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

print(parsed_response["Time Series (Daily)"]["2019-02-19"]["4. close"])
# > '1627.5800'


#
# INFO OUTPUTS
#

# csv-mgmt/write_teams.py

print("--------------------------------")
print("SELECTED SYMBOL: MSFT")
print("--------------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("--------------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"THE LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("--------------------------------")
print("RECOMMENDATION: BUY!") # TODO
print("BECAUSE: TODO") # TODO
print("--------------------------------")
print("HAPPY INVESTING") 
print("--------------------------------")

csv_file_path = "prices.csv" # a relative filepath

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader() # uses fieldnames set above
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})

#
# BUT THE LATEST DAY WON'T ALWAYS BE "2019-02-19"
# ... SO HERE'S A WAY TO GET THE LATEST DAY, WHATEVER IT IS
#

#
# What keys or attributes does this dictionary have?
# ... see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md


#
# print(parsed_response["Time Series (Daily)"][latest_day]["4. close"])
# > '1627.5800'
#
# print(tsd[latest_day]["4. close"])
# > '1627.5800'
