from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, DateField,
                     PasswordField, SubmitField, BooleanField)
from wtforms.validators import (Optional, DataRequired, Length, Email, EqualTo)


class SignupForm(FlaskForm):
    username: StringField = StringField("Username", validators=[
        DataRequired(), Length(2, 20)])
    email: StringField = StringField(
        "Email", validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField(
        "Password", validators=[DataRequired(), Length(8, 16)])
    confirm_password: PasswordField = PasswordField("Confirm password", validators=[
                                                    DataRequired(), Length(8, 16), EqualTo("password")])
    gender: SelectField = SelectField("Gender", choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[Optional()])
    dob: DateField = DateField(
        "Date of Birth", validators=[Optional()], format='%Y-%m-%d', default=datetime.now())
    submit: SubmitField = SubmitField("Sign up")


class LoginForm(FlaskForm):
    email: StringField = StringField(
        "Email", validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField(
        "Password", validators=[DataRequired(), Length(8, 16)])
    remember_me: BooleanField = BooleanField("Remember Me")
    submit: SubmitField = SubmitField("Login")
