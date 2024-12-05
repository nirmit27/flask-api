from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from .forms import LoginForm, SignupForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()

        if user and check_password_hash(user.password, login_form.password.data):
            flash(f"Welcome back, {login_form.username.data}!", category="success")

            login_user(user, remember=True)
            return redirect(url_for("view.home"))  # redirecting to the home page

        flash("Invalid username or password.")

    return render_template("login.html", form=login_form)  # login form


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        hashed_password = generate_password_hash(
            signup_form.password.data, method="pbkdf2", salt_length=16
        )
        new_user = User(username=username, email=email, password=hashed_password)  # type: ignore

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for("auth.login"))  # redirecting to the login page

    return render_template("signup.html", form=signup_form)  # sign-up form


@auth_bp.route("/logout")
def logout():
    logout_user()

    flash("Logged out successfully.")
    return redirect(url_for("auth.login"))  # redirecting to the login page
