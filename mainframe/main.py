from abc import abstractclassmethod, abstractmethod
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import datetime as d
import time
import pytz
from os import path
import mysql.connector as mysql
from mysql.connector import MySQLConnection
import datetime
from threading import Thread, Event
import threading
import json


class SystemManager:
    """
    Responsability: To handle request from flask script called stockfluent_main.pyu to the main python script, main.py. It forwards the request to apropiate component interface.
    """

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
    """
    Responsability: To handle all communication with the databse and therfore it is the only object thats knows about the database and its procedures
    """

    def __init__(self, dbconnector):
        self.connector = dbconnector

    def create_user(self, email, password):
        '''If the email doesn't already exist, returns the new users userID. Else returns None.'''
        return self.connector.data_handler("insertUser", [email, password])

    def check_login(self, username, password):
        "get connection, then call apropiate procedure"
        x = self.connector.data_handler("logIn", [username, password])
        a = [x[0][0], x[1][0]]
        print(a)
        return a

    def get_user_settings(self, username):
        "get connection, then call apropiate procedure"
        pass

    def set_user_settings(self, username, settings):
        "get connection, then call apropiate procedure"
        pass

    def get_stockdata(self, stock_ID, nbr_of_data_points, interval):
        "get connection, then call apropiate procedure"
        return self.connector.data_handler("getStockData", [stock_ID, nbr_of_data_points, interval])

    def set_stockdata(self, stock_list):
        "get connection, then call apropiate procedure"
        for items in stock_list[0].keys():
            self.connector.data_handler("insertStockData", [
                                        stock_list[1]['2. Symbol'], items, stock_list[0][items]["4. close"]])

    def get_recommendations(self, stockId, interval):
        # print(self.connector.data_handler('getRecommendation', [stockId, interval]))
        # print(self.connector.data_handler('getRecommendation', ["AAPL", "1min"]))
        # recommendation= [('Bullich', 122.0561, datetime.datetime(2021, 3, 18, 12, 45), 'AAPL', '15min'), ('Bearich', 120.2099, datetime.datetime(2021, 3, 19, 11, 15), 'TSLA', '20min'), ('kallek', 120.2099, datetime.datetime(2021, 3, 19, 11, 20), 'AMZN', '15min'), ('Buy', 1.0561, datetime.datetime(2021, 3, 18, 11, 43), 'AAPL', '15min'), ('Sell', 122.0561, datetime.datetime(2021, 5, 17, 12, 45), 'AAPL', '1min')]
        return self.connector.data_handler('getRecommendation', [stockId, interval])
        # return recommendation

    def set_recommendation(self, algoID, recommendation):
        self.connector.data_handler('insertRecommendation', [
                                    algoID, recommendation["date"], recommendation["recAction"], recommendation["price"]])
        print("Set_recommendation")
        "get connection, then call apropiate procedure"

    def set_algorithm(self, settings):
        ''' Returns a list with the algoID on the first position and a bool telling if the algorithm already existed or not'''
        algoID = self.connector.data_handler('setAlgorithm', [settings])
        return algoID

    def check_mail_existence(self, email):
        "get connection, then call apropiate procedure"
        x = self.connector.data_handler('emailExists', [email])
        return x[0][0]

    def change_password(self, email, new_password):
        "ny metod som elion kom på"
        "get connection, then call apropiate procedure"
        return self.connector.data_handler('changePassword', [new_password, email])[0]

    def set_reset_code(self, email, code):
        self.connector.data_handler('setResetCode', [email, code])

    def ping_echo(self):
        "get connection, then call apropiate procedure"
        pass


class DatabaseConnector:
    """
    Responsability: To establish connection with the database
    """

    def __init__(self, username, password):
        self.connection = None
        self.lock = threading.Lock()

    def data_handler(self, func, arg=None):
        self.lock.acquire()
        if not self.connection:
            self.connection = MySQLConnection(
                host='localhost', database='StockFluent', user='root')
        cnx = self.connection.cursor(dictionary=True)
        if arg == None:
            cnx.callproc(func)

        else:
            cnx.callproc(func, arg)
        result = []
        for items in cnx.stored_results():
            result.append(items.fetchall()[0])
        self.connection.commit()
        # self.connection.close()
        self.lock.release()
        return result

# Profile component


class ProfileInterface:
    """
    Responsability: To handle all communication with the profile component.
    """

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
    ''' The controller of the algorithm moduel. Knows the algortims that are running and starts and create the algoritms
    Responsability: To handle all communication with the recommendation component.
    '''

    def __init__(self, databaseInterface):
        self.avalible_algo = []
        self.db_interface = databaseInterface
        self.my_algo_collection = {
            "MACD": ["stock, interval, fastperiod, slowperiod, signalperiod"]}
        # tillfällig lösning för mvp, kan tas bort när vi kan hämta api resultatet från databas

    def get_available_algortihms(self):
        return self.my_algo_collection

    def get_algo_settings(self, algo_type):
        return self.my_algo_collection[algo_type]

    def _create_algo(self, algoID, settings):
        if settings["result"]["algo_type"] == "MACD":
            new_algo = MACD(settings, self.db_interface, algoID)
            self.avalible_algo.append(new_algo)
            return new_algo

        elif settings["result"]["algo_type"] == "RSI":
            new_algo = RSI(settings, self.db_interface, algoID)
            self.avalible_algo.append(new_algo)
            return new_algo

    def run_algorithm(self, settings):
        b = json.dumps(settings)
        a = self.db_interface.set_algorithm(b)
        # a en lista med algoid och True False [algoID,Bool]
        # if not a[1][0]:
        algo = self._create_algo(a[0][0], settings)
        algo.start()
        return a[0][0]

    def kill(self, algoID):
        for algo in self.avalible_algo:
            if algoID == algo.get_ID():
                algo.kill()

        # return "Message from backend"


class Algorithm(Thread):
    '''abstract algoritm class not fully implemented'''
    @abstractmethod
    def __init__(self, settings, DB, algoID):
        Thread.__init__(self)
        self.alive = True
        self.settings = settings
        self.db_interface = DB
        self.algoID = algoID

    @abstractmethod
    def recommendationLogic(self, settings, stock_info):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def kill(self):
        self.alive = False

    @abstractmethod
    def is_alive(self):
        return self.alive


class MACD(Algorithm):
    def __init__(self, settings, DB, algoID):
        super().__init__(settings, DB, algoID)
        ''' Gives the user recomendations when the market is bearich, Bullich, when to sell and when to buy'''

        '''" The algoritm settings coming in from the website interface
        MACD", {"result": {"stock": stockName, "interval": interval,
                                            "fastperiod": fPeriod, "slowperiod": sPeriod, "signalperiod": lPeriod}}'''

    def run(self):
        i = 0
        while self.alive == True and i < 1:
            result = self.db_interface.get_stockdata(
                self.settings["result"]["stock"], self.settings["result"]["slowperiod"]+1, self.settings["result"]["interval"])
            resultErlier = result[1:]
            date, closePrice, fastEMAList, slowEMAList, signalLine = self.unpackData(
                result)
            dateErlier, closePriceErlier, fastEMAListErlier, slowEMAListErlier, signalLineErlier = self.unpackData(
                resultErlier)
            MACD_Hist = self.create_Hist(
                closePrice, fastEMAList, slowEMAList, signalLine)
            MACD_HistErlier = self.create_Hist(
                closePriceErlier, fastEMAListErlier, slowEMAListErlier, signalLineErlier)
            recommendation = self.recommendationLogic(
                MACD_Hist, MACD_HistErlier, closePrice, date)
            self.db_interface.set_recommendation(self.algoID, recommendation)
            time.sleep(10)
            i += 1

    def unpackData(self, data):
        fastEMAList = []
        slowEMAList = []
        signalLine = []
        date = data[0][0]
        date = date.strftime('%Y-%m-%d %H:%M')
        closePrice = data[0][1]
        fastdata = data[:self.settings["result"]["fastperiod"]]
        slowdata = data[:self.settings["result"]["slowperiod"]]
        signalLinedata = data[:self.settings["result"]["signalperiod"]]
        for value in fastdata:
            fastEMAList.append(value[1])
        for value in slowdata:
            slowEMAList.append(value[1])
        for value in signalLinedata:
            signalLine.append(value[1])
        return date, closePrice, fastEMAList, slowEMAList, signalLine

    def create_Hist(self, closingPrice, fastEMAList, slowEMAList, signalLine):
        ''' signal line return the Histogram value in the MACD algoritm'''
        fastAvrege = sum(fastEMAList)/len(fastEMAList)
        slowAvrege = sum(slowEMAList)/len(slowEMAList)
        signalAvrege = sum(signalLine)/len(signalLine)
        fastEMA = closingPrice * 2 / \
            len(fastEMAList)+fastAvrege*(1-(2/(len(fastEMAList)+1)))
        slowEMA = closingPrice * 2 / \
            len(slowEMAList)+slowAvrege*(1-(2/(len(slowEMAList)+1)))
        MACD = fastEMA-slowEMA
        Hist = MACD - signalAvrege
        return Hist

    def recommendationLogic(self, MACD_Hist, MACD_HistErlier, stock_price, date):
        '''The lodgic behind the recomendations. If the Histogram
        is 0 it is time to buy or sell,
        If the Histogram is positive it is bull market and
        if negative it is bear market'''

        if MACD_Hist > 0 and (MACD_Hist and MACD_HistErlier > 0):
            rec = Recommendation(
                "Bullich", stock_price, date, self.settings)
            return rec.get_recomendation_info()

        elif MACD_Hist < 0 and (MACD_Hist and MACD_HistErlier < 0):
            rec = Recommendation(
                "Bearich", stock_price, date, self.settings)
            return rec.get_recomendation_info()

        elif (MACD_Hist == 0 and MACD_HistErlier > 0) or (MACD_Hist >= 0 and MACD_HistErlier <= 0):
            rec = Recommendation("Sell", stock_price, date, self.settings)
            return rec.get_recomendation_info()

        elif (MACD_Hist == 0 and MACD_HistErlier < 0) or (MACD_Hist >= 0 and MACD_HistErlier <= 0):
            rec = Recommendation("Buy", stock_price, date, self.settings)
            return rec.get_recomendation_info()


class RSI(Algorithm):
    '''settings {nrPeriod:5 periodLength:1min buySignal:30 sellSignal:70}'''

    def __init__(self, settings, DB, algoID):
        super().__init__(settings, DB, algoID)

    def run(self):
        i = 0
        while self.alive == True and i < 1:
            '''get nrPeriod st List med periodlength mellanrum'''
            dataList = self.db_interface.get_stockdata(
                self.settings["result"]["stock"], self.settings["result"]["nrPeriod"]+1, self.settings["result"]["interval"])
            dataList, closingPrice, date = self.unpackData(dataList)
            avregeGain, avregeLoss = 0, 0
            for data in dataList:
                avrege = data[0]-data[-1]
                if avrege >= 0:
                    avregeGain += abs(avrege)
                else:
                    avregeLoss += abs(avrege)
            if avregeLoss != 0:
                RS = avregeGain/avregeLoss
                RSI = 100 - (100/(1+(RS)))
            else:
                RSI = 100
            recommendation = self.recommendationLogic(RSI, closingPrice, date)
            self.db_interface.set_recommendation(self.algoID, recommendation)
            time.sleep(10)
            i += 1

    def unpackData(self, data):
        date = data[0][0]
        date = date.strftime('%Y-%m-%d %H:%M')
        closePrice = data[0][1]
        dataList = []
        for priceIndex in range(len(data)-1):
            pricePair = []
            priceF = data[priceIndex][1]
            priceS = data[priceIndex+1][1]
            pricePair.append(priceF)
            pricePair.append(priceS)
            dataList.append(pricePair)
        return dataList, closePrice, date

    def recommendationLogic(self, RSI, stock_price, date):
        '''The lodgic behind the recomendations. If the RSI
        is bellow buySignal settings it is time to buy and 
        if it is over sellSignal it is time to sell'''

        if RSI < self.settings["result"]["buySignal"]:
            rec = Recommendation("Buy", stock_price, date, self.settings)
            return rec.get_recomendation_info()

        elif RSI > self.settings["result"]["sellSignal"]:
            rec = Recommendation("Sell", stock_price, date, self.settings)
            return rec.get_recomendation_info()


class FibonacciRetracement(Algorithm):
    #not implemented
    def __init__(self):
        pass


class Recommendation:
    '''create the recomendation from the algoritm'''

    def __init__(self, recAction, stock_price, stock_date, settings):
        self.recAction = recAction
        self.stock_price = stock_price
        self.stock_date = stock_date
        self.settings = settings

    def get_recomendation_info(self):
        print({"recAction": self.recAction, "price": self.stock_price,
               "settings": self.settings, "date": self.stock_date})
        return{"recAction": self.recAction, "price": self.stock_price, "settings": self.settings, "date": self.stock_date}


# StockdataCollector
"kanske kan lösa denna implementation bättre StockdataInterface bara refererar vidare"


class StockdataInterface:
    """
    Responsability: To handle all communication with the stock data component.
    """

    def __init__(self, databaseInterface, api_connector):
        self.db_interface = databaseInterface
        self.my_api_connector = api_connector
        # self.dataFormater = DataFormater()

    # def get_macd_intraday(self, algo_type, settings):
    #     """Tillfällig metod för att lösa mvp, gör två anrop till api och ersätter där med while loopen i RecommendationInteface"""
    #     result = settings["result"]

    #     MACD_stockinfo = self.my_api_connector.get_macd(
    #         result["stock"], result["interval"], result["fastperiod"], result["slowperiod"], result["signalperiod"])
    #     stock_info = self.my_api_connector.get_intraday(
    #         result["stock"], result["interval"])
    #     # kallar på data formateraren och sparar resultat
    #     formatted_data = self.dataFormater.format_data(
    #         MACD_stockinfo, stock_info, settings["result"]["interval"])
    #     formatted_data.append(settings)
    #     return formatted_data

    def macd(self, stock, time_interval):
        return self.my_api_connector.get_macd(stock, time_interval)

    def days(self, stock):
        return self.my_api_connector.get_days(stock)

    def get_intraday(self, stock):
        self.db_interface.set_stockdata(
            self.my_api_connector.get_intraday(stock))


class ApiConnector:
    """
    Responsability: To connecto to the alpha vantage api.
    """

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

    def get_intraday(self, stock):
        """"interval: '1min', '5min', '15min', '30min', '60min'"""
        return self.time_app.get_intraday(stock, '1min', outputsize="full")


# class DataFormater:
#     def __init__(self) -> None:
#         pass

#     def format_data(self, MACD_stock_info, stock_info, interval):
#         # Unpacks the data and gets the MACD_Histogram data and data from the MACD_Histogram 1 min eralier
#         macdData = MACD_stock_info
#         date = self.fixTime(interval)

#         # felhantering
#         date -= d.timedelta(hours=1)
#         date -= d.timedelta(days=3)
#         # in parameter tids intervall
#         dateErlier = date - d.timedelta(minutes=int(interval[:-3]))
#         date1 = date.strftime('%Y-%m-%d %H:%M:00')
#         date = date.strftime('%Y-%m-%d %H:%M')
#         dateErlier = dateErlier.strftime('%Y-%m-%d %H:%M')
#         macd_dateInfo = macdData[0][date]
#         macd_dateInfoErlier = macdData[0][dateErlier]
#         MACD_Hist = float(macd_dateInfo["MACD_Hist"])
#         MACD_HistErlier = float(macd_dateInfoErlier["MACD_Hist"])
#         stockPrice = float(stock_info[0][date1]["4. close"])
#         return [MACD_Hist, MACD_HistErlier, stockPrice, date1]

#     def fixTime(self, interval):
#         currentTime = d.datetime.today()
#         tmp = currentTime.time().minute
#         a = tmp//int(interval[:-3])
#         currentTime = currentTime.replace(minute=a*int(interval[:-3]))
#         currentTime = currentTime.replace(second=0, microsecond=0)
#         return currentTime


def setUp():
    """An initializing setup method, instances all necessary objects for testing with website"""
    apiConnector = ApiConnector("PFHGI45JG5C2X5DQ")
    dbConnector = DatabaseConnector("usr", "psw")
    dbInterface = DatabaseInterface(dbConnector)
    stockInterface = StockdataInterface(dbInterface, apiConnector)
    proInter = ProfileInterface(dbInterface)
    recInter = RecommendationInterface(dbInterface)
    sysManager = SystemManager(proInter, recInter, stockInterface)
    return sysManager, dbInterface


if __name__ == "__main__":
    # api_key = "PFHGI45JG5C2X5DQ"
    # test = ApiConnector(api_key)
    # databaseInterface = DatabaseInterface(DatabaseConnector("usr", "psw"))
    # # test with Apple stock and 5min interval
    # # print(test.get_macd("AAPL", "5min"))
    # test2 = StockdataInterface("databaseInterface", ApiConnector(api_key))
    # test3 = RecommendationInterface("databaseInterface", test2)

    api_key = "PFHGI45JG5C2X5DQ"
    test = ApiConnector(api_key)
    DB = DatabaseInterface(DatabaseConnector("usr", "psw"))
    SDI = StockdataInterface(DB, ApiConnector(api_key))
    # SDI.get_intraday("AAPL")
    test3 = RecommendationInterface(DB)
    a = test3.run_algorithm({"result": {"algo_type": "RSI",
                                        "stock": "AAPL", "nrPeriod": 5, "interval": "0:01", "buySignal": 30, "sellSignal": 40}})
    b = test3.run_algorithm({"result": {"algo_type": "MACD",
                                        "stock": "AAPL", "interval": "0:01", "fastperiod": 1, "slowperiod": 2, "signalperiod": 3}})
    # c = test3.run_algorithm("MACD", {"result": {
    #     "stock": "AAPL", "interval": "1min", "fastperiod": 1, "slowperiod": 2}})
    # print(c)
    # print(threading.active_count())
    # dbConnector = DatabaseConnector("usr", "psw")
    # dbInterface = DatabaseInterface(dbConnector)
    # a = RSI()
    # a.run_recomendation(
    #     {"nrPeriod": 3, "periodLength": "1min", "buySignal": 30, "sellSignal": 70})
# {"MACD", {"result": {
#         "stock": "AAPL", "interval": "1min", "fastperiod": 2, "slowperiod": 6, "signalperiod": 9}: MACD()}

    # test with Apple stock and 5min interval
    # print(test.get_macd("AAPL", "5min"))
    # test2 = StockdataInterface(databaseInterface, ApiConnector(api_key))
    # test3= RecommendationInterface("databaseInterface", test2)
    # test3.run_algorithm("MACD", {"result": {"stock": "AAPL", "interval": "1min",
    # "fastperiod": 12, "slowperiod": 26, "signalperiod": 9}})
    # dbConnector = DatabaseConnector("usr", "psw")
    # dbInterface = DatabaseInterface(dbConnector)
    # test2.get_intraday('AAPL')
    # print(databaseInterface.get_stockdata('AAPL', 3, '0:10'))
