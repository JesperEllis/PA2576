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

    if stockName and interval:
        interface = manager.get_recommendation_interface()
        x = interface.run_algorithm("MACD", interval, stockName)

        return render_template('algorithm.html') + x
    else:
        return render_template('algorithm.html')

@app.route("/Recommendations/")
def recommendation():
    return render_template("recommendation.html")

if __name__ == "__main__":
    manager = main.setUp()
    app.run(debug=True)