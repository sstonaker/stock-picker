from bs4 import BeautifulSoup as BS
import requests


def convert_notation(notation):
    # Convert ie. 1.04B to 1040000000
    if notation[-1] == 'T':
        notation = int(float(notation[0:-1]) * 1_000_000_000_000)
    elif notation[-1] == 'B':
        notation = int(float(notation[0:-1]) * 1_000_000_000)
    elif notation[-1:] == 'M':
        notation = int(float(notation[0:-1]) * 1_000_000)
    elif notation[-1:] == 'K':
        notation = int(float(notation[0:-1]) * 1_000)
    else:
        try:
            # if the value is small, it might not have a denomination
            # ie. 1000
            notation = int(notation)
        except:
            try:
                # account for a value not included above (T, B, M, K)
                if notation[-1] == type(str):
                    notation = notation[0:-1]
            except:
                # return None so we can assume if the value is None, it
                # is missing or wasn't parsed correctly.
                # We will check before calculations that the value exists
                # None will be excluded rather than interrupt with an error
                return None
    return notation


def parse_elements(stock_data, price_data):
    """From the two lists generated from the html elements, parse the items of interest into
    values of specified type to create Stock object.

    This uses absolute references, but the references should be the same for each ticker scraped. A null value
    will be stored as None which can be checked before attempting a calculation.

    Most values scraped will be a string with surrounding data of the numerical value we are interested in.
    ie. opening price -> "Open $123.40" we will use replace to replace the leading test with no text ('') leaving
    only the numerical value.

    Other functions to remove special character such as percentages, letter denominations, commas, etc. are detailed below.

    Args:
        stock_data (list): List generated by scraper containing left elements of MarketWatch financial data.
        price_data (list): List generated by scraper containing right elements of MarketWatch historical price data.

    Yields:
        tuple: ticker, day_open, day_range_low, day_range_high, fiftytwo_low, fiftytwo_high,
        market_cap, shares_outstanding, public_float, beta, rev_per_emp, pe_ratio, eps,
        stock_yield, dividend, ex_dividend, short_interest, percent_float, avg_volume,
        five_day, one_month, three_month, ytd, one_year
    """
    ticker = stock_data[0]
    day_open = make_float(stock_data[1].replace('Open $', ''))
    day_range = stock_data[2].replace('Day Range ', '').split()
    day_range_low = make_float(day_range[0])
    day_range_high = make_float(day_range[2])
    fiftytwo_week_range = stock_data[3].replace('52 Week Range ', '').split()
    fiftytwo_low = make_float(fiftytwo_week_range[0])
    fiftytwo_high = make_float(fiftytwo_week_range[2])
    market_cap = convert_notation(stock_data[4].replace('Market Cap $', ''))
    shares_outstanding = convert_notation(
        stock_data[5].replace('Shares Outstanding ', ''))
    public_float = convert_notation(stock_data[6].replace('Public Float ', ''))
    beta = make_float(stock_data[7].replace('Beta ', ''))
    rev_per_emp = convert_notation(
        stock_data[8].replace('Rev. per Employee $', ''))
    pe_ratio = make_float(stock_data[9].replace('P/E Ratio ', ''))
    eps = make_float(stock_data[10].replace('EPS $', ''))
    stock_yield = remove_percent(stock_data[11].replace('Yield ', ''))
    dividend = make_float(stock_data[12].replace('Dividend $', ''))
    ex_dividend = stock_data[13].replace('Ex-Dividend Date ', '')
    short_interest_str = stock_data[14].replace('Short Interest ', '').split()
    short_interest = convert_notation(short_interest_str[0])
#    short_interest_date = short_interest[1] - no current use for a short interest date
    percent_float = remove_percent(
        stock_data[15].replace('% of Float Shorted ', ''))
    avg_volume = convert_notation(
        stock_data[16].replace('Average Volume ', ''))
    five_day = remove_percent(price_data[43])
    one_month = remove_percent(price_data[45])
    three_month = remove_percent(price_data[47])
    ytd = remove_percent(price_data[49])
    one_year = remove_percent(price_data[51])

    return ticker, day_open, day_range_low, day_range_high, fiftytwo_low, fiftytwo_high, market_cap, shares_outstanding, public_float, beta, rev_per_emp, pe_ratio, eps, stock_yield, dividend, ex_dividend, short_interest, percent_float, avg_volume, five_day, one_month, three_month, ytd, one_year


def scrape(ticker):
    # Scrape financial and price history data from MarketWatch.com pages and store html elemtns in two lists
    # from which we will parse data
    stock_data = []
    price_data = []
    url = (
        f"https://www.marketwatch.com/investing/stock/{ticker}?mod=quote_search")
    print(f"\nRequesting info for {ticker}...")
    page = requests.get(url)
    # Right now this just prints a message so the user can see it is working
    # once the list exports to json, this can be used to confirm the page was
    # retrieved successfully for debugging purposes.
    if page.status_code == 200:
        print(f"OK")

    soup = BS(page.content, 'html.parser')
    print("Creating soup...")
    # Left table in the "overview" section
    elements_left = soup.find_all('li', class_='kv__item')
    # Right table in the overview section
    elements_right = soup.find_all('td', class_='table__cell')

    # Store the ticker as the first item in the list
    stock_data.append(ticker)

    for li in elements_left:
        # format the elements and append each to the list after the ticker
        element = li.get_text().replace('\n', ' ')
        stock_data.append(element.strip())

    for tr in elements_right:
        # format the elements and append each to the list
        element = tr.get_text()
        price_data.append(element.strip())

    # Call the function to parse the raw text items into useful data and types
    parsed_data = parse_elements(stock_data, price_data)
    print(f"Parsing {ticker} data...\n")

    # Returns a tuple containing the parsed data
    return parsed_data


def remove_percent(percentage):
    # removes the % sign at the end of a value
    # ie. 7.08% -> 7.08
    percentage = percentage[0:-1]
    try:
        return float(percentage)
    except:
        return None


def make_float(data):
    # for values > 999, removes "," char and
    # converts string to a float
    # ie. 1,234.56 -> 1234.56
    try:
        return float(data.replace(',', ''))
    except:
        return None
