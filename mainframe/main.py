from abc import abstractclassmethod, abstractmethod
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import datetime as d
import time
import pytz
from os import path
import mysql.connector as mysql
from sshtunnel import SSHTunnelForwarder


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

    def get_recommendations(self, stockId, interval):
        return self.connector.data_handler('getRecommendation', [stockId, interval])

    def set_recommendation(self, recommendation):
        print(recommendation)
        self.connector.data_handler('insertRecommendation', [recommendation["recAction"], recommendation["price"], recommendation["date"],
                                                             recommendation["settings"]["result"]["stock"], recommendation["settings"]["result"]["interval"]])
        print("Set_recommendation")
        "get connection, then call apropiate procedure"

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
        self.SSH_USER = 'jeeu18'  # ACRONYM
        self.SSH_PASS = 'ForTheDatabase123'  # CANVAS_PASS

        self.MYSQL_USER = self.SSH_USER  # ACRONYM
        self.MYSQL_PASS = 'CZEf69snXtUA'  # MYSQL_PASS
        self.MYSQL_DATABASE = self.SSH_USER  # ACRONYM

    def data_handler(self, func, arg=None):
        print(self.SSH_USER)
        filtered_prod = 0
        with SSHTunnelForwarder(
                ('ssh.student.bth.se', 22),
                ssh_username=self.SSH_USER,
                ssh_password=self.SSH_PASS,
                remote_bind_address=('blu-ray.student.bth.se', 3306)
        ) as tunnel:
            connection = mysql.connect(host='127.0.0.1', user=self.MYSQL_USER,
                                       passwd=self.MYSQL_PASS, db=self.MYSQL_DATABASE, port=tunnel.local_bind_port)
            print("Sent_function")
            cnx = connection.cursor(dictionary=True)

            if arg == None:
                cnx.callproc(func)

            else:
                cnx.callproc(func, arg)

            for row in cnx.stored_results():
                filtered_prod = row.fetchall()
            connection.commit()
            connection.close()

            return filtered_prod


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

    def __init__(self, databaseInterface, stockdataInterface):

        self.db_interface = databaseInterface
        self.my_algo_collection = {
            "MACD": ["stock, interval, fastperiod, slowperiod, signalperiod"]}
        #tillfällig lösning för mvp, kan tas bort när vi kan hämta api resultatet från databas
        self.my_stockdata_interface = stockdataInterface

    def get_available_algortihms(self):
        return self.my_algo_collection

    def get_algo_settings(self, algo_type):
        return self.my_algo_collection[algo_type]

    def _create_algo(self, algo_type):
        if algo_type == "MACD":
            self.algo_type = MACD()

    def run_algorithm(self, algo_type, settings):

        formatted_list = self.my_stockdata_interface.get_macd_intraday(algo_type, settings)
        #kan skriva detta direkt som in parameterar men skrev så här för tydlighetens skull
        macd_hist = formatted_list[0]
        macd_hist_erlier = formatted_list[1]
        stock_price = formatted_list[2]
        date = formatted_list[3]
        settings = formatted_list[4]
        algo_to_run = self._create_algo(algo_type)
        algo_to_run.recommendationLogic(macd_hist, macd_hist_erlier, stock_price, date, settings)

        return "Message from backend"


class Algorithm:
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def recommendationLogic(self, settings, stock_info):
        raise NotImplementedError

class MACD(Algorithm):
    def __init__(self):
        # Gives the user recomendations when the market is bearich, Bullich, when to sell and when to buy
        pass

    def recommendationLogic(self, MACD_Hist, MACD_HistErlier, stock_price, date1, settings):
        '''The lodgic behind the recomendations. If the Histogram
        is 0 it is time to buy or sell,
        If the Histogram is positive it is bull market and
        if negative it is bear market'''

        if MACD_Hist > 0 and (MACD_Hist and MACD_HistErlier > 0):
            rec = Recommendation(
                "Bullich", stock_price, date1, settings)
            return rec.get_recomendation_info()

        elif MACD_Hist < 0 and (MACD_Hist and MACD_HistErlier < 0):
            rec = Recommendation(
                "Bearich", stock_price, date1, settings)
            return rec.get_recomendation_info()

        elif (MACD_Hist == 0 and MACD_HistErlier > 0) or (MACD_Hist >= 0 and MACD_HistErlier <= 0):
            rec = Recommendation("Sell", stock_price, date1, settings)
            return rec.get_recomendation_info()

        elif (MACD_Hist == 0 and MACD_HistErlier < 0) or (MACD_Hist >= 0 and MACD_HistErlier <= 0):
            rec = Recommendation("Buy", stock_price, date1, settings)
            return rec.get_recomendation_info()


class Recommendation:
    # prints recomendations
    def __init__(self, recAction, stock_price, stock_date, settings):
        self.recAction = recAction
        self.stock_price = stock_price
        self.stock_date = stock_date
        self.settings = settings

    def get_recomendation_info(self):
        return{"recAction": self.recAction, "price": self.stock_price, "settings": self.settings, "date": self.stock_date}


# StockdataCollector
"kanske kan lösa denna implementation bättre StockdataInterface bara refererar vidare"


class StockdataInterface:
    def __init__(self, databaseInterface, api_connector):
        self.db_interface = databaseInterface
        self.my_api_connector = api_connector
        self.dataFormater = DataFormater()

    def get_macd_intraday(self, algo_type, settings):
        """Tillfällig metod för att lösa mvp, gör två anrop till api och ersätter där med while loopen i RecommendationInteface"""
        result = settings["result"]

        MACD_stockinfo = self.my_api_connector.get_macd(
                result["stock"], result["interval"], result["fastperiod"], result["slowperiod"], result["signalperiod"])
        stock_info = self.my_api_connector.get_intraday(
                result["stock"], result["interval"])
        #kallar på data formateraren och sparar resultat
        formatted_data = self.dataFormater.format_data(MACD_stockinfo, stock_info)
        formatted_data.append(settings)
        return formatted_data
        
        

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

class DataFormater:
    def __init__(self) -> None:
        pass

    def format_data(self, MACD_stock_info, stock_info):
        # Unpacks the data and gets the MACD_Histogram data and data from the MACD_Histogram 1 min eralier
        macdData = MACD_stock_info
        date = d.datetime.today()
        date -= d.timedelta(hours=5)
        date -= d.timedelta(days=1)
        dateErlier = date - d.timedelta(minutes=1)
        date1 = date.strftime('%Y-%m-%d %H:%M:00')
        date = date.strftime('%Y-%m-%d %H:%M')
        dateErlier = dateErlier.strftime('%Y-%m-%d %H:%M')
        macd_dateInfo = macdData[0][date]
        macd_dateInfoErlier = macdData[0][dateErlier]
        MACD_Hist = float(macd_dateInfo["MACD_Hist"])
        MACD_HistErlier = float(macd_dateInfoErlier["MACD_Hist"])
        stockPrice = float(stock_info[0][date1]["4. close"])
        return [MACD_Hist, MACD_HistErlier, stockPrice, date1]


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
    test2 = StockdataInterface("databaseInterface", ApiConnector(api_key))
    test3= RecommendationInterface("databaseInterface", test2)
    test3.run_algorithm("MACD", {"result": {"stock": "AAPL", "interval": "1min",
                            "fastperiod": 12, "slowperiod": 26, "signalperiod": 9}})
