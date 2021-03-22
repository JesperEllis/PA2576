from flask import Flask, redirect, url_for, render_template, request
import main
import mysql.connector
import importlib
import datetime
import re

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/Algorithm/", methods=["POST", "GET"])
def algorithm():
    stockName = request.args.get("stockID")
    interval = request.args.get("interval")
    fPeriod = request.args.get("fPeriod")
    sPeriod = request.args.get("sPeriod")
    lPeriod = request.args.get("lPeriod")

    if stockName and interval:
        interface = manager.get_recommendation_interface()
        x = interface.run_algorithm("MACD", {"result": {"stock": stockName, "interval": interval,
                                            "fastperiod": fPeriod, "slowperiod": sPeriod, "signalperiod": lPeriod}})
        return render_template("algorithm.html") + "<div class=bg-light mt-5><p>"+x+"</p</div>"
    else:
        return render_template('algorithm.html')


@app.route("/Recommendations/")
def recommendation():
    """Take in stock info from the datebase and render it on the website"""
    
    ticket = request.args.get("stockID")
    interval2 = request.args.get("interval")

    

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

        return render_template('recommendation.html', listDictonary=listDictonary) #Skickat in listan listDictonary i html
    else:
        return render_template('recommendation.html')

@app.route("/Profile/", methods=['POST', 'GET'])
def profile(): #Hur når jag create_user härifrån??? #Nästa sak som jag ska fixa
    #dbInterface.create_user()
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #kalla på create_user
        #create_user(email, password)
        #print (username, password)
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "pass", database = "ProjektDatabas") #Ansluter till databasen
        cur = myconn.cursor() # det är en cursor, pekare av något slag
        sql = "insert into user (email, password) VALUES (%s, %s)" #Sätter in email och password i SQL databasen, med strängar
        val = (email, password) #Det som hamnar i %s och %s
        cur.execute(sql, val) #Execute, slår ihop SQL och val och får en komplett query
        myconn.commit() # lägger in det i databasen
        myconn.close() #stänger databasen
        return f'({email}, {password})' #Skriver ut detta på hemsidan
    return render_template("profile.html")

if __name__ == "__main__":
    manager,dbInterface = main.setUp()
    app.run(debug=True)




