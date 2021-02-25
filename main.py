import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

api_key = "PFHGI45JG5C2X5DQ"

class ApiRequest:
    def __init__(self, api_key):
        """Api objects instanciated with api_key"""
        self.time_app = TimeSeries(api_key)
        self.tech_app = TechIndicators(api_key , output_format = "pandas") #can change the output_format to json which is default
 
    def get_macd(self, stock, time_interval):
        """
        Returns macd_signal, macd, macd_hist
        Interval: '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly'
        """
        return self.tech_app.get_macd(stock, interval=time_interval, series_type = "close")

    def get_days(self, stock):
        """Returns timeseries with close-value each day (20 years back)"""
        return self.time_app.get_daily(stock)

    def get_intraday(self, stock, time_interval):
        """"interval: '1min', '5min', '15min', '30min', '60min'"""
        return self.time_app.get_intraday(stock, time_interval)


if __name__ == "__main__":
    test = ApiRequest(api_key)
    #test with Apple stock and 5min interval
    print(test.get_macd("AAPL", "5min"))