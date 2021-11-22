class Stock:
    def __init__(self, parsed_data):
        # Assign the passed tuple to attributes of the Stock object representing
        # useful financial data and price history of a company
        self.ticker = parsed_data[0]
        self.day_open = parsed_data[1]
        self.day_range_low = parsed_data[2]
        self.day_range_high = parsed_data[3]
        self.fiftytwo_low = parsed_data[4]
        self.fiftytwo_high = parsed_data[5]
        self.market_cap = parsed_data[6]
        self.shares_outstanding = parsed_data[7]
        self.public_float = parsed_data[8]
        self.beta = parsed_data[9]
        self.rev_per_emp = parsed_data[10]
        self.pe_ratio = parsed_data[11]
        self.eps = parsed_data[12]
        self.stock_yield = parsed_data[13]
        self.dividend = parsed_data[14]
        self.ex_dividend = parsed_data[15]
        self.short_interest = parsed_data[16]
        self.percent_float = parsed_data[17]
        self.avg_volume = parsed_data[18]
        self.five_day = parsed_data[19]
        self.one_month = parsed_data[20]
        self.three_month = parsed_data[21]
        self.ytd = parsed_data[22]
        self.one_year = parsed_data[23]

        # Flags for calculated values on how we will identify properties of interest
        self.watch_list = False
        self.growth = False
        self.value = False
        self.buy = False
        self.sell = False

    def review(self):
        """Work in progress. We will implement a financial review to determine if this stock meets certain
        investment criteria.
        """
        if self.market_cap and self.market_cap > 1_000_000_000:
            if self.day_open and self.day_open > ((self.fiftytwo_high + self.fiftytwo_low) / 2):
                if self.pe_ratio and self.pe_ratio > 1:
                    if self.one_year and self.one_year > 20:
                        self.watch_list = True
