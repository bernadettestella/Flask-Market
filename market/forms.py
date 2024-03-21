from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    
    # Ensures the username entered is unique
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists')
        
    # Ensures the email adress provided is unique
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists')
            
    username = StringField("Username", validators=[length(min=2, max=30), DataRequired()])
    email = StringField("Email Address", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[length(min=6), DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField("Create Account")
    
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
    
class PurchaseItemForm(FlaskForm):
    submit = SubmitField("Purchase Item")
    
class SellItemForm(FlaskForm):
    submit = SubmitField("Sell Item")