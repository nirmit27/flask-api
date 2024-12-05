from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 16)])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), Length(8, 16), EqualTo("password")],
    )
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 16)])
    submit = SubmitField("Log in")
