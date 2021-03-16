from abc import abstractclassmethod, abstractmethod
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

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

#Storage component
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

#Profile component
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

#Recommendation component
class RecommendationInterface:
    def __init__(self, databaseInterface):
        self.db_interface = databaseInterface
        self.my_algo_collection = {}

    def get_available_algortihms(self):
        return self.my_algo_collection

    def get_algo_settings(self, algo_type):
        return self.my_algo_collection[algo_type].get_settings()
    
    def run_algorithm(self, algo_type, settings, stockinfo):
        self.my_algo_collection[algo_type].create_recommendation(settings, stockinfo)
        return "result"

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
        super().__init__()
        "lägg in i listan här "
        self.possibel_settings = []
    
    def create_recommendation(self, settings, stock_info):
        "Edvin lägg in dit här"
        pass

class Recommendation:
    def __init__(self, stock_name, stock_price, recommendation):
        self.recommendation = recommendation
        self.stock_name = stock_name
        self.stock_price = stock_price

#StockdataCollector
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
    api_key = "PFHGI45JG5C2X5DQ"
    test = ApiConnector(api_key)
    #test with Apple stock and 5min interval
    print(test.get_macd("AAPL", "5min"))

    