
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask.helpers import flash
import main
import mysql.connector
import importlib
import datetime
import re
from mailsender import MailSender

app = Flask(__name__)
app.secret_key = "sotck45&%204()ON)????=)(/&&"
#plt.style.use('fivethirtyeight')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/Algorithm")
def Algorithm():   
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
        # Denna variabel avgör vad för meddelande som ska visas på hemsidan, sätt till danger om algo ej körde pga fel
        cat = "success"
    return render_template('macd.html', message=msg, category=cat)


@app.route("/Algorithm/RSI")
def RSI():
    return "RSI"


@app.route("/Algorithm/Algo3")
def Algo3():
    return "Algo 3"

@app.route("/Recommendations")
def recommendation():
    """Take in stock info from the datebase and render it on the website"""

    ticket = request.args.get("stockID")
    interval2 = request.args.get("interval")

    if ticket and interval2:
        recommendationFromMain = dbInterface.get_recommendations(
            ticket, interval2)
        listDictonary = []
        listOfKey = ["ReAction", "Price", "Date", "StockId",
                     "Interval"]  # Hur datan ser ut innan loop
        # print(recommendationFromMain)
        for dataInList in recommendationFromMain:
            date = str(dataInList[2]).split(' ')[0]  # Tar ut datum
            time = str(dataInList[2]).split(' ')[1]  # Tar ut tid
            zipbObj = zip(listOfKey, dataInList)  # Zipar ihop listorna,
            dictOfWords = dict(zipbObj)  # Skapar en dictionary från zip objekt
            # Lägger till datumet sist i dictionary
            dictOfWords['oDate'] = date
            dictOfWords['oTime'] = time
            # Lägger till dictionay i en list
            listDictonary.append(dictOfWords)

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

        # Skickat in listan listDictonary i html
        return render_template('recommendation.html', listDictonary=listDictonary)
    else:
        return render_template('recommendation.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db_result = dbInterface.check_login(email, password)
        if db_result[0]:
            user = User(email, id=db_result[1])
            user.set_authentication(True)
            login_user(user)
            
            next = request.args.get("next")

            return redirect(url_for("Profile"))

        return render_template("login.html", incorrect = True)

    else: 
        return render_template("login.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if dbInterface.check_mail_existence(email):
            return render_template("signup.html", exists = True)
        
        #stores user in DB
        dbInterface.create_user(email, password)
        return render_template("login.html")
        
    else:
        return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user(current_user)################################
    users_lst.remove(current_user)#############################
    flash("You have been logged out!")
    return redirect(url_for("home"))

@app.route("/Profile")
@login_required
def Profile():
    print(current_user.is_active())
    usid = str(current_user.get_id())
    return render_template("profile.html") + current_user._email + usid

login_manager = LoginManager()
login_manager.init_app(app)

class User:
    def __init__(self, email, id):
        self._email = email
        self.authenticated = False
        self.id = id        
        self.active = False
        self.anonymous = False
        #Tillfällig lösning
        users_lst.append(self)
    
    def set_authentication(self, auth_bool):
        self.authenticated = auth_bool
    
    def is_authenticated(self):
        return self.active
    
    def is_active(self):
        return self.active
    
    def is_anonymous(self):
        return self.anonymous
    
    def get_id(self):
        """Return a unicode object that repsresents the users id"""
        return self.id

#Tillfällig lösning ska egentligen sparas i DATABAS
users_lst = []
user_emails = {"test@bth.se": User("test@bth.se", "pass")}

@login_manager.user_loader
def load_user(user_id):
    for i in range(0, len(users_lst, -1)):
        if user_id == users_lst[i].get_id():
            return users_lst[i]
    return None


if __name__ == "__main__":
    manager, dbInterface = main.setUp()
    app.run(debug=True)
