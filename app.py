import json
from time import sleep
from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

# Page Routes


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", title="Home")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html", title="About")


@app.route("/employees", methods=["GET"])
def employees():
    data: dict[int, dict] = {}
    with open("data.json", 'r') as fp:
        data = json.load(fp)

    return render_template("employees.html", title="Employees", data=data)


@app.route("/careers", methods=["GET"])
def careers():
    return render_template("careers.html", title="Careers")


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html", title="Contact Us")

# Misc. Routes


@app.route("/welcome/<string:name>", methods=["GET"])
def welcome(name):
    return f"<h1>Welcome, {name.title()}!</h1>"


@app.route("/even-odd/<int:num>", methods=["GET"])
def square(num):
    return render_template("even-odd.html", title="Even-Odd", num=num)


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
