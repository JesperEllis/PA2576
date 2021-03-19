from flask import Flask, redirect, url_for, render_template, request
import main
import mysql.connector

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
        x = interface.run_algorithm("MACD", {"result": {"stock": stockName, "interval": "1min",
                                            "fastperiod": fPeriod, "slowperiod": sPeriod, "signalperiod": lPeriod}})
        return render_template("algorithm.html") + x
    else:
        return render_template('algorithm.html')


@app.route("/Recommendations/")
def recommendation():
    return render_template("recommendation.html")

@app.route("/Profile/", methods=['POST', 'GET'])
def profile(): #Hur når jag create_user härifrån???
    main.dbInterface.create_user()
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
    manager = main.setUp()
    app.run(debug=True)
