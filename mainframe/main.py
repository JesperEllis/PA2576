from abc import abstractclassmethod, abstractmethod
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import datetime as d
import time
import pytz


class SystemManager:
    def __init__(self, prointer, recointer, stointer):
        self.profileinter = prointer
        self.recommendationinter = recointer
        self.stockdatainter = stointer

    def get_recommendation_interface(self):
        return self.recommendationinter

    def get_profile_interface(self):
        return self.profileinter

    def get_stockdata_interface(self):
        return self.stockdatainter

# Storage component


class DatabaseInterface:
    def __init__(self, dbconnector):
        self.connector = dbconnector

    def create_user(self, email, password):
        pass

    def check_login(self, username, password):
        "get connection, then call apropiate procedure"
        pass

    def get_user_settings(self, username):
        "get connection, then call apropiate procedure"
        pass

    def set_user_settings(self, username, settings):
        "get connection, then call apropiate procedure"
        pass

    def get_stockdata(self, stock_name):
        "get connection, then call apropiate procedure"
        pass

    def set_stockdata(self, stock_name, stock_info):
        "get connection, then call apropiate procedure"
        pass

    def get_recommendations(self, stock_name):
        "get connection, then call apropiate procedure"
        pass

    def set_recommendation(self, recommendation):
        "get connection, then call apropiate procedure"
        print(recommendation)
        pass

    def check_mail_existence(self, email):
        "get connection, then call apropiate procedure"
        pass

    def change_password(self, email, new_password):
        "ny metod som elion kom på"
        "get connection, then call apropiate procedure"
        pass

    def ping_echo(self):
        "get connection, then call apropiate procedure"
        pass


class DatabaseConnector:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Profile component


class ProfileInterface:
    def __init__(self, databaseInterface):
        self.db_interface = databaseInterface
        self.active_users = []
        self.mail_sender = MailSender()

    def create_user(self, email, password):
        self.db_interface.creat_user(email, password)

    def login(self, email, password):
        self.db_interface.check_login(email, password)
        self.active_users.append(email)

    def logout(self, email):
        "kanske borde spara pofile data i detta stadie"
        self.active_users.remove(email)

    def reset_password(self, email):
        self.db_interface.check_mail_existence(email)
        self._send_mail(email, "reset_pass")

    def _send_mail(self, email, cause):
        "ny som elion kom på"
        self.mail_sender.send_email(email, cause)

    def update_password(self, email, new_pawwsord):
        self.db_interface.change_password(email, new_pawwsord)

    def set_profile_algo(self, email, algo_type, algo_settings):
        pass


class MailSender:
    def send_email(self, email, mail_cause):
        pass

# Recommendation component


class RecommendationInterface:
    def __init__(self, API, databaseInterface):
        self.db_interface = databaseInterface
        self.API = API
        self.my_algo_collection = {
            "MACD": ["stock, interval, fastperiod, slowperiod, signalperiod"]}

    def get_available_algortihms(self):
        return self.my_algo_collection

    def get_algo_settings(self, algo_type):
        return self.my_algo_collection[algo_type]

    def _create_algo(self, algo_type):
        if algo_type == "MACD":
            self.algo_type = MACD()

    def run_algorithm(self, algo_type, settings):
        print(settings)
        result = settings["result"]
        rec = 0
        while rec <= 1:
            MACD_stockinfo = self.API.get_macd(
                result["stock"], result["interval"], result["fastperiod"], result["slowperiod"], result["signalperiod"])
            stock_info = self.API.get_intraday(
                result["stock"], result["interval"])
            self._create_algo(algo_type)
            recomendation = self.algo_type.create_recommendation(
                settings, MACD_stockinfo, stock_info)
            self.db_interface.set_recommendation(recomendation)
            time.sleep(60)
            rec += 1
        #self.my_algo_collection[algo_type].create_recommendation(settings, stockinfo)
        return "Message from backend"


class Algorithm:
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def create_recommendation(self, settings, stock_info):
        raise NotImplementedError

    @abstractmethod
    def get_possible_settings(self):
        raise NotImplementedError


class MACD(Algorithm):
    def __init__(self):
        # super().__init__()
        # Gives the user recomendations when the market is bearich, Bullich, when to sell and when to buy
        self.MACD_Hist = None
        self.MACD_HistErlier = None

    def create_recommendation(self, settings, MACD_stock_info, stock_info):
        # runs the algorithm.
        self._unpackData(MACD_stock_info, stock_info)
        recomendation = self._recomendationLogic(
            self.MACD_Hist, self.MACD_HistErlier, settings)
        return recomendation

    def _unpackData(self, MACD_stock_info, stock_info):
        # Unpacks the data and gets the MACD_Histogram data and data from the MACD_Histogram 1 min eralier
        self.macdData = MACD_stock_info
        self.date = d.datetime.today()
        self.date -= d.timedelta(hours=5)
        self.date -= d.timedelta(days=1)
        self.dateErlier = self.date - d.timedelta(minutes=1)
        self.date1 = self.date.strftime('%Y-%m-%d %H:%M:00')
        self.date = self.date.strftime('%Y-%m-%d %H:%M')
        self.dateErlier = self.dateErlier.strftime('%Y-%m-%d %H:%M')
        self.macd_dateInfo = self.macdData[0][self.date]
        self.macd_dateInfoErlier = self.macdData[0][self.dateErlier]
        self.MACD_Hist = float(self.macd_dateInfo["MACD_Hist"])
        self.MACD_HistErlier = float(self.macd_dateInfoErlier["MACD_Hist"])
        self.stockPrice = float(stock_info[0][self.date1]["4. close"])

    def _recomendationLogic(self, MACD_Hist, MACD_HistErlier, settings):
        '''The lodgic behind the recomendations. If the Histogram
        is 0 it is time to buy or sell,
        If the Histogram is positive it is bull market and
        if negative it is bear market'''

        if MACD_Hist > 0 and (MACD_Hist and MACD_HistErlier > 0):
            rec = Recommendation(
                "Bullich", self.stockPrice, self.date1, settings)
            return rec.get_recomendation_info()

        elif MACD_Hist < 0 and (MACD_Hist and MACD_HistErlier < 0):
            print("Bearich print")
            rec = Recommendation(
                "Bearich", self.stockPrice, self.date1, settings)
            return rec.get_recomendation_info()

        elif (MACD_Hist == 0 and MACD_HistErlier > 0) or (MACD_Hist >= 0 and MACD_HistErlier <= 0):
            rec = Recommendation("Sell", self.stockPrice, self.date1, settings)
            return rec.get_recomendation_info()

        elif (MACD_Hist == 0 and MACD_HistErlier < 0) or (MACD_Hist >= 0 and MACD_HistErlier <= 0):
            rec = Recommendation("Buy", self.stockPrice, self.date1, settings)
            return rec.get_recomendation_info()


class Recommendation:
    # prints recomendations
    def __init__(self, recAction, stock_price, stock_date, settings):
        self.recAction = recAction
        self.stock_price = stock_price
        self.stock_date = stock_date
        self.settings = settings

    def get_recomendation_info(self):
        return{"recAction": self.recAction, "price": self.stock_date, "settings": self.settings, "date": self.stock_date}


# StockdataCollector
"kanske kan lösa denna implementation bättre StockdataInterface bara refererar vidare"


class StockdataInterface:
    def __init__(self, databaseInterface, api_connector):
        self.db_interface = databaseInterface
        self.my_api_connector = api_connector

    def macd(self, stock, time_interval):
        return self.my_api_connector.get_macd(stock, time_interval)

    def days(self, stock):
        return self.my_api_connector.get_days(stock)

    def get_intraday(self, stock, time_interval):
        return self.my_api_connector.get_intraday(stock, time_interval)


class ApiConnector:
    def __init__(self, api_key):
        """Api objects instanciated with api_key"""
        self.key = api_key
        self.time_app = TimeSeries(api_key)
        # can change the output_format to json which is default
        self.tech_app = TechIndicators(api_key, output_format="json")

    def get_macd(self, stock, time_interval, fastperiod, slowperiod, signalperiod):
        """
        Returns macd_signal, macd, macd_hist
        Interval: '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly'
        """
        return self.tech_app.get_macd(stock, interval=time_interval, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod, series_type="close")

    def get_days(self, stock):
        """Returns timeseries with close-value each day (20 years back)"""
        return self.time_app.get_daily(stock)

    def get_intraday(self, stock, time_interval):
        """"interval: '1min', '5min', '15min', '30min', '60min'"""
        return self.time_app.get_intraday(stock, time_interval, outputsize="full")


def setUp():
    """An initializing setup method, instances all necessary objects for testing with website"""
    apiConnector = ApiConnector("PFHGI45JG5C2X5DQ")
    dbConnector = DatabaseConnector("usr", "psw")
    dbInterface = DatabaseInterface(dbConnector)
    stockInterface = StockdataInterface(dbInterface, apiConnector)
    proInter = ProfileInterface(dbInterface)
    recInter = RecommendationInterface(apiConnector, dbInterface)
    sysManager = SystemManager(proInter, recInter, stockInterface)
    return sysManager


if __name__ == "__main__":
    api_key = "PFHGI45JG5C2X5DQ"
    test = ApiConnector(api_key)
    # test with Apple stock and 5min interval
    # print(test.get_macd("AAPL", "5min"))
    dbConnector = DatabaseConnector("usr", "psw")
    databaseInterface = DatabaseInterface(dbConnector)
    test2 = RecommendationInterface(ApiConnector(api_key), databaseInterface)
    test2.run_algorithm("MACD", {"result": {"stock": "AAPL", "interval": "1min",
                                            "fastperiod": 12, "slowperiod": 26, "signalperiod": 9}})
