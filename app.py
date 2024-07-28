import os
from dotenv import load_dotenv
from forms import SignupForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, url_for, redirect, flash, session, request

load_dotenv()

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Dummy creds.
user: str
pwd: str

# Page Routes


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", title="Home")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        global user
        global pwd

        user = signup_form.username.data or ""
        pwd = generate_password_hash(
            signup_form.password.data, method='scrypt') or ""
        
        session["username"] = user
        flash(f"Successfully registered as {user}!")

        return redirect(url_for("index", username=user))

    return render_template("signup.html", title="Sign Up", form=signup_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        global user
        global pwd

        username: str = login_form.username.data or ""
        password: str = login_form.password.data or ""

        if username == user and check_password_hash(pwd, password):
            session["username"] = user
            flash(f"Welcome back, {user}!")

            return redirect(url_for("index", username=user))
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
        return redirect(url_for("login", next=request.url))


if __name__ == '__main__':
    app.run(debug=True)
