from dow30 import dow30
from nasdaq100 import nasdaq100
from stock import Stock
from ticker_scraper import scrape

# Assign ticker or list of tickers
# common tickers from Dow 30 and Nasdaq 100 available as
# dow30 and nasdaq100, respectively.
# ex. dow30, nasdaq100, ["AAPL"], ["AAPL", "AMZN", "MSFT"]
tickers = ["AAPL", "AMZN", "MSFT"]


# An empty list in which we will store the stock objects
stocks = []

# A watch list of stocks that meet the criter of the Stock.review() method.
# see stock.py for details.
watch_list = []


for ticker in tickers:
    # iterate through the list of tickers and scrape the data. The scrape() function will
    # parse, format, and attempt to type or return a null value for each item. Returns a tuple which
    # will be used to generate the Stock object from the Stock class.
    data = scrape(ticker)
    # prints the data for now, but this can be removed eventually
    print(data)
    stocks.append(Stock(data))

for stock in stocks:
    # Calls the [for now rudimentary] review method on each stock object to see if it meets investment
    # critera, if so, it will change the stock.watch_list boolean to True and append to watch list.
    stock.review()
    if stock.watch_list:
        watch_list.append(stock)

for stock in watch_list:
    # Print some general information for the stocks that passed the .review() method criteria.
    print(f"{stock.ticker} | MKT CAP: {stock.market_cap} | YTD: {stock.ytd}")

# Just for curiosity, print the number of stocks that made the watch list.
# This can be used to tune the .review() method.
# Too many results means the criteria is too loose, too little means the
# criteria is too strict.
print(f"{len(watch_list)} of {len(stocks)} on watch list")
