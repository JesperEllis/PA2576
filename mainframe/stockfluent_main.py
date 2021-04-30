from flask import Flask, redirect, url_for, render_template, request, session
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
        #interface.run_algorithm({"result": {"algo_type": "MACD", "stock": stockName, "interval": interval,
        #                                   "fastperiod": fPeriod, "slowperiod": sPeriod, "signalperiod": lPeriod}}) För att kunna testa hemsidan
        msg = "The algortihm is running and you can see the results in the"
        # Denna variabel avgör vad för meddelande som ska visas på hemsidan, sätt till danger om algo ej körde pga fel
        cat = "success"
    return render_template('macd.html', message=msg, category=cat)

@app.route("/Algorithm/RSI")
def RSI():
    stockName = request.args.get("stockID")
    interval = request.args.get("interval")
    period = request.args.get("period")
    overbought = request.args.get("overbought")
    oversold = request.args.get("oversold")
    msg = None
    cat = None

    if stockName and interval:
        interface = manager.get_recommendation_interface()
        #interface.run_algorithm({"result": {"algo_type":"RSI",
        #                    "stock": stockName,"nrPeriod": period, "interval": interval, "buySignal": oversold, "sellSignal": overbought}})
        msg = "The algortihm is running and you can see the results in the"
        # Denna variabel avgör vad för meddelande som ska visas på hemsidan, sätt till danger om algo ej körde pga fel
        cat = "success"
    return render_template('rsi.html', message=msg, category=cat)


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

        # Skickat in listan listDictonary i html
        return render_template('recommendation.html', listDictonary=listDictonary)
    else:
        return render_template('recommendation.html')

@app.route("/login", methods=['POST', 'GET'])
def login(): #Hur når jag create_user härifrån??? #Nästa sak som jag ska fixa
    #dbInterface.create_user()
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

@app.route("/password_reset", methods=['POST', 'GET'])
def password_reset():
    if request.method == 'POST':
        email = request.form['email']
        try:
            code = mail_sender.reset_password(email)
            dbInterface.set_reset_code(email, code)
            flash('Mail has been sent to '+email+'!')
        except Exception:
            pass
        return redirect(url_for('new_password'))
    
    return render_template('password_reset.html')

@app.route("/new_password", methods=['POST', 'GET'])
def new_password():
    if request.method == 'POST':
        code = request.form['code']
        newPassword = request.form['password']

        if dbInterface.change_password(code, newPassword):
            flash('Password successfully changed!')
            return redirect('login')

        msg = 'Code is incorrect, try again!'
        return render_template("new_password.html", message = msg)

    return render_template("new_password.html")


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
    logout_user()
    for user in users_lst:
        if user.get_id()==current_user.get_id():
            users_lst.remove(user)
            break
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
    print(user_id, users_lst)
    for i in range( len(users_lst) -1 , 0, -1):
        print(users_lst[i].get_id())
        if user_id == users_lst[i].get_id():
            return users_lst[i]
    return None


if __name__ == "__main__":
    manager,dbInterface = main.setUp()
    mail_sender = MailSender()
    app.run(debug=True)
