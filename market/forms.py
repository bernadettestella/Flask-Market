from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists')
        
        
    username = StringField("Username", validators=[length(min=2, max=30), DataRequired()])
    email = StringField("Email Address", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[length(min=6), DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField("Create Account")