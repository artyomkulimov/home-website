from os import name
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField,FileRequired
from werkzeug.utils import secure_filename

class RegistrationForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired(),Length(min = 2,max=20)])
    email = StringField("Email:",validators=[DataRequired(),Email()])
    password = PasswordField("Password:",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:",validators=[DataRequired(), EqualTo('password')])
    file = FileField("Add your Profile Picture")
    submit = SubmitField("Register", validators=[FileRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired(),Length(min = 2,max=20)])
    password = PasswordField("Password:",validators=[DataRequired()])
    submit = SubmitField("Register")
