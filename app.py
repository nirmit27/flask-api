from time import sleep
from flask import Flask, render_template, url_for, redirect, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return "<h1>Home Sweet Home!</h1>"


@app.route("/welcome/<string:name>", methods=["GET"])
def welcome(name):
    return f"<h1>Welcome, {name.title()}!</h1>"


@app.route("/square/<int:num>", methods=["GET"])
def square(num):
    return f"<h1>{num} squared equals {num ** 2}</h1>"


@app.route("/sum/<int:num1>/<int:num2>", methods=["GET"])
def sum(num1, num2):
    return f"<h1>{num1} + {num2} = {num1 + num2}</h1>"


@app.route("/eligible/<string:name>/<int:age>")
def eligible(name, age):
    return f"<h1>{name.title()} (aged {age} yrs.), you are ELIGIBLE to cast a vote.</h1>"


@app.route("/inligible/<string:name>/<int:age>")
def inligible(name, age):
    return f"<h1>{name.title()} (aged {age} yrs.), you are INLIGIBLE to cast a vote.</h1>"


@app.route("/judge/<string:name>/<int:age>")
def judge(name, age):
    sleep(1)
    if age >= 18:
        return redirect(url_for("eligible", name=name, age=age))
    else:
        return redirect(url_for("inligible", name=name, age=age))


if __name__ == "__main__":
    app.run(debug=True)
