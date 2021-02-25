import yfinance as yf

class StockData:
    def __init__(self, stock_ticker):
        self.stock_data = yf.Ticker(stock_ticker)

    def get_moving_avg(self, interval):
        return self.stock_data.info[interval]

    def get_price(self):
        return self.stock_data.info["previousClose"]


class Algo:
    def __init__(self, stock_data, interval = "fiftyDayAverage", ema_interval = None, signal_line = None):
        "algo Settings"
        self.interval = interval
        self.ema_interval = ema_interval
        self.signal_line = signal_line
        self.data_getter = stock_data #<StockData>

        
    def generate_reco(self):
        "nothing fancy, just basic start"
        #Gets moving avg at given time interval
        avg_price = self.data_getter.get_moving_avg(self.interval)
        market_price = self.data_getter.get_price()
        #takes action
        if market_price > avg_price:
            print(f"buy!!,price: {market_price}, avg price: {avg_price}")
            return "Buy"
        print(f"sell!!,price: {market_price}, avg price: {avg_price}")
        return "Sell"

if __name__ == "__main__":
    std = StockData("AAPL")
    algo_1 = Algo(stock_data=std)
    algo_1.generate_reco()


    #####test