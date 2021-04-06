from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask.helpers import flash
import main
import mysql.connector
import importlib
import datetime
import re
#import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import random



app = Flask(__name__)
app.secret_key = "sotck45&%204()ON)????=)(/&&"
#plt.style.use('fivethirtyeight')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/Algorithm", methods=["GET", "POST"] )
def Algorithm():
    if request.method == "POST":
        if request.form["algo"] == "MACD":
            return redirect(url_for("MACD"), code=302)
        elif request.form["algo"] == "Algo 2":
            return redirect(url_for("Algo2"), code=302)
        elif request.form["algo"] == "Algo 3":
            return redirect(url_for("Algo3"), code=302)
            
    return render_template("algorithm.html")


@app.route("/Algorithm/MACD", methods=["POST", "GET"])
def MACD():
    stockName = request.args.get("stockID")
    interval = request.args.get("interval")
    fPeriod = request.args.get("fPeriod")
    sPeriod = request.args.get("sPeriod")
    lPeriod = request.args.get("lPeriod")
    msg = None
    cat = None

    if stockName and interval:
        interface = manager.get_recommendation_interface()
        # interface.run_algorithm("MACD", {"result": {"stock": stockName, "interval": interval,
        #                                     "fastperiod": fPeriod, "slowperiod": sPeriod, "signalperiod": lPeriod}}) För att kunna testa hemsidan
        msg = "The algortihm is running and you can see the results in the"
        #Denna variabel avgör vad för meddelande som ska visas på hemsidan, sätt till danger om algo ej körde pga fel
        cat = "success"
    return render_template('macd.html', message= msg, category=cat)

@app.route("/Algorithm/Algo2")
def Algo2():
    return "Algo 2"

@app.route("/Algorithm/Algo3")
def Algo3():
    return "Algo 3"

@app.route("/Recommendations/")
def recommendation():
    """Take in stock info from the datebase and render it on the website"""

    
    ticket = request.args.get("stockID") 
    interval2 = request.args.get("interval")
    if interval2 not in locals(): #Om man inte har valt ett intervall och tid kommer det då bli
        ticket = 'AAPL'
        interval2 = '15min'

    if ticket and interval2:
        recommendationFromMain = dbInterface.get_recommendations(ticket, interval2)
        listDictonary = []
        listOfKey = ["ReAction", "Price", "Date", "StockId", "Interval"] #Hur datan ser ut innan loop
        #print(recommendationFromMain)
        for dataInList in recommendationFromMain:
            date = str(dataInList[2]).split(' ')[0] #Tar ut datum
            time = str(dataInList[2]).split(' ')[1] #Tar ut tid
            zipbObj = zip(listOfKey, dataInList) #Zipar ihop listorna, 
            dictOfWords = dict(zipbObj) #Skapar en dictionary från zip objekt
            dictOfWords['oDate'] = date #Lägger till datumet sist i dictionary
            dictOfWords['oTime'] = time
            listDictonary.append(dictOfWords) #Lägger till dictionay i en list
        print(listDictonary)
        
        yValue = []
        xValue = []
        """
        for random_number in random.sample(range(1, 30), 20): 
            yValue.append(random_number)
            #print(yValue)
        print(yValue)

        for random_number in random.sample(range(1, 30), 20): 
            xValue.append(random_number)
            #print(xValue)
        print(xValue)"""
        
        
        for i in listDictonary:
            if i['ReAction'] == 'Buy' or i['ReAction'] =='Sell':
                xValue.append(i['Price'])
                yValue.append(i['oTime'])
        print (yValue)

        return render_template('recommendation.html', listDictonary=listDictonary, xValue=xValue, yValue= yValue) #Skickat in listan listDictonary i html
    else:
        return render_template('recommendation.html')
"""
def graph(listDictonary):
    print("hhhhhhhheeeeeeejjjjjj")
    xValues = []
    yValues = []
    xValues.append([d['oTime'] for d in listDictonary])
    yValues.append([d['Price'] for d in listDictonary])
    print(xValues)
    plt.cla()
    plt.plot(xValues[0], yValues[0], label='pris')

def updateGraph():
    ani = FuncAnimation(plt.gcf(), graph, interval = 1000)    
    plt.tight_layout()
    plt.show() """




@app.route("/Profile/", methods=['POST', 'GET'])
def profile(): #Hur når jag create_user härifrån??? #Nästa sak som jag ska fixa
    #dbInterface.create_user()
    cat = None
    msg = None
    
    if request.method == 'POST':
        email = request.form['text']
        password = request.form['password']
        #kalla på create_user
        #create_user(email, password)
        #print (username, password

        # Bort kommenterat för att testa hemsida#############################################################################################
        # myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "pass", database = "ProjektDatabas") #Ansluter till databasen
        # cur = myconn.cursor() # det är en cursor, pekare av något slag
        # sql = "insert into user (email, password) VALUES (%s, %s)" #Sätter in email och password i SQL databasen, med strängar
        # val = (email, password) #Det som hamnar i %s och %s
        # cur.execute(sql, val) #Execute, slår ihop SQL och val och får en komplett query
        # myconn.commit() # lägger in det i databasen
        # myconn.close() #stänger databasen

        #Denna variabel avgör vad för meddelande som ska visas på hemsidan, sätt till danger om det är fell inlogg
        cat = "success"
        
        return render_template("profile.html", category = cat, message = email)

    return render_template("profile.html")

if __name__ == "__main__":
    manager,dbInterface = main.setUp()
    app.run(debug=True)





