import os

from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from forms import SignupForm, LoginForm

from model import User, db

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app=app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # type: ignore
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", title="Home")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        password = generate_password_hash(
            signup_form.password.data, method='scrypt')
        gender = signup_form.gender.data
        dob = signup_form.dob.data

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            flash("Username or email already taken. Please choose a different one.")
            return redirect(url_for("signup"))

        new_user = User(username=username, email=email,
                        password=password, gender=gender, dob=dob) # type: ignore
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(f"Successfully registered and logged in as {username}!")

        return redirect(url_for("index", username=username))

    return render_template("signup.html", title="Sign Up", form=signup_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        remember = login_form.remember_me.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.username}!")

            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index", username=user.username))
        else:
            flash("Incorrect username or password!")

    return render_template("login.html", title="Log In", form=login_form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/u/<string:username>")
@login_required
def index(username: str):
    if current_user.username == username:
        return render_template("index.html", title=f"Overview | {username}", username=username)
    else:
        flash("Unauthorized access!")
        return redirect(url_for("login", next=request.url))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
