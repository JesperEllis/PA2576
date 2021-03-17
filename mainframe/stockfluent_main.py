from flask import Flask, redirect, url_for, render_template, request
import main2

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

        return render_template('algorithm.html') + x + " based on " + stockName +" "+ interval
    else:
        return render_template('algorithm.html')

@app.route("/Recommendations/")
def recommendation():
    return render_template("recommendation.html")

if __name__ == "__main__":
    manager = main2.setUp()
    app.run(debug=True)