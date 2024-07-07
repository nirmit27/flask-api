from flask import Flask, render_template, url_for, redirect, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
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


if __name__ == "__main__":
    app.run(debug=True)
