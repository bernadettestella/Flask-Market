from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, EqualTo, Email, DataRequired

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[length(min=2, max=30), DataRequired()])
    email = StringField("Email Address", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[length(min=6), DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField("Create Account")