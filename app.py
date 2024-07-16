import os
from dotenv import load_dotenv
from forms import SignupForm, LoginForm
from flask import Flask, render_template, url_for, redirect, flash, session, request

load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Dummy creds.
uname: str = os.environ.get("TEST_UNAME") or "demo_user"
pwd: str = os.environ.get("TEST_PWD") or "pwd12345"

# Page Routes


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", title="Home")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        username: str = signup_form.username.data

        flash(f"Successfully registered as {username}!")
        return redirect(url_for("index", username=username))

    return render_template("signup.html", title="Sign Up", form=signup_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username: str = login_form.username.data
        password: str = login_form.password.data

        if username == uname and password == pwd:
            session["username"] = username
            flash(f"Welcome back, {username}!")
            return redirect(url_for("index", username=username))
        else:
            flash(f"Incorrect username or password!")

    return render_template("login.html", title="Log In", form=login_form)


@app.route("/logout/")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/u/<string:username>")
def index(username: str):
    if session["username"] == username:
        username = session["username"]
        return render_template("index.html", title=f"Overview | {username}", username=username)
    else:
        flash("Please log in first!")
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
