import os
from dotenv import load_dotenv
from forms import SignupForm, LoginForm
from flask import Flask, render_template, url_for, redirect, request

load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Page Routes


@app.route("/", methods=["GET", "POST"])
@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form: SignupForm = SignupForm()
    ...
    return render_template("signup.html", title="Sign Up", form=signup_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form: LoginForm = LoginForm()
    ...
    return render_template("login.html", title="Login", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
