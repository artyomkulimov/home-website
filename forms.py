from os import name
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField,FileRequired
from werkzeug.utils import secure_filename
from __main__ import User

class RegistrationForm(FlaskForm):
    username = StringField("Username:",validators = [DataRequired(),Length(min = 2,max=20)])
    email = StringField("Email:", validators=[DataRequired(),Email()])
    password = PasswordField("Password:",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:",validators=[DataRequired(), EqualTo('password')])
    # file = FileField("Add your Profile Picture")
    submit = SubmitField("Register")
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError(message="The username is already taken")
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError(message="The email is already in use")

class LoginForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired(),Length(min = 2,max=20)])
    password = PasswordField("Password:",validators=[DataRequired()])
    submit = SubmitField("Register")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username:", validators = [Length(min = 2,max=20),DataRequired()])
    email = StringField("Email:",validators=[Email(),DataRequired()])
    pfp = FileField("Add your Profile Picture", validators=[FileAllowed(["jpg","png","jpeg"])])
    submit = SubmitField("Submit")
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError(message="The username is already taken")
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError(message="The email is already in use")