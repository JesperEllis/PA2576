from flask import Flask, redirect, url_for, render_template, request
import main

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


if __name__ == "__main__":
    manager = main.setUp()
    app.run(debug=True)
