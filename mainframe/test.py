import mysql.connector as mysql
from mysql.connector import MySQLConnection
import datetime
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
# def connect():
    # """ Connect to MySQL database """
    # conn = None
    # try:
    #     conn = mysql.connect(host='localhost',
    #                                    database='StockFluent',
    #                                    user='root')
    #     if conn.is_connected():
    #         print('Connected to MySQL database')

conn = MySQLConnection(host='localhost',database ='StockFluent', user = 'root')
cursor = conn.cursor(dictionary=True)


cursor.callproc("getStockData",['AAPL', 3, '0:02'])
result = []

for items in cursor.stored_results():
    result.append(items.fetchall())
    
print(result)
api_key = "PFHGI45JG5C2X5DQ"
time_app = TimeSeries(api_key)

tmpList = []
tmp = time_app.get_intraday('AAPL', '1min', outputsize="compact")
for items in tmp[0].keys():
    cursor.callproc("insertStockData",['AAPL',items,tmp[0][items]["4. close"]])
    conn.commit()
# for items in tmp:
#     print(items.keys())
# .get_intraday("MACD", {"result": {"stock": "AAPL", "interval": "1min"}}))

# get closingPrice, date, fastEMAList, slowEMAList, closingpriceErlier, fastEMAListErlier, slowEMAListErlier