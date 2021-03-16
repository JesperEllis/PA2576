from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/Algorithm/", methods=["POST", "GET"])
def algorithm():
    test = request.args.get("nm", "")

    return(
        render_template("algorithm.html")+test
    )


@app.route("/Recommendations/")
def recommendation():
    return render_template("recommendation.html")

if __name__ == "__main__":
    app.run(debug=True)

