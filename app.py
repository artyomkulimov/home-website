from flask import Flask,render_template,url_for,redirect,flash, jsonify, request
from flask_bcrypt import Bcrypt
from flask_login import login_manager, login_user, current_user, logout_user, LoginManager, UserMixin
from flask_login.mixins import UserMixin
from flask_login.utils import login_required
from wtforms.validators import Email
from forms import RegistrationForm,LoginForm
import os
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.datastructures import Headers
from flask_sqlalchemy import SQLAlchemy, model


app = Flask(__name__)
app.config["SECRET_KEY"] = 'FLASK_SECRET_KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),nullable = True)
    email = db.Column(db.String(30),nullable = True)
    password = db.Column(db.String(20),nullable = True)
    pfp = db.Column(db.String(100),nullable = False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html",title = "Home",Header = "<h1>Website Blog</h1>")

@app.route("/credits")
def credits():
    return render_template("credits.html",title = "Credits",Header = "This is the credits page")

@app.route("/form")
def form():
    return render_template("form.html",title = "Form")

@app.route("/updates")
def updates():
    return render_template("updates.html",title = "Updates",Header = "This is where I document updates to my github page.")

@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("UTF-8")
        # filename = form.file.name
        # print(filename)
        # form.file.data.save('\profile_pictures'+ filename)
        # filename = secure_filename(form.file.data.filename)
        # form.file.data.save('uploads/' + filename)
        file = request.files['file']
        file.save(secure_filename(file.filename))
        user = User(username = form.username.data,email = form.email.data, password = hash_password,pfp = file)
        db.session.add(user)
        db.session.commit()
        flash(f"Account was created for user {form.username.data}","success") 
        return redirect(url_for("home"))
    return render_template("register.html",form = form,title = "Register",Header = "This is the registration Form")

@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user)
            flash(f"You have been logged in to {form.username.data}","success") 
            return redirect(url_for("home"))
        else:
            flash(f"Either username or password incorrect","inv-cred")
    return render_template("login.html",form = form,title = "Login",Header = "This is the Login page")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    if request.method == 'POST':
        file = request.files['file']
        file.save(secure_filename(file.filename))
        return 'file uploaded successfully'
    return render_template("modify_account.html")
    

@app.route('/upload')
@login_required
def file_upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
@login_required
def download_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(secure_filename(file.filename))
        user = User(pfp = file.filename)
        db.session.add(user)
        db.session.commit()
        return render_template("account.html")
    




if __name__ == "__main__":
    app.run(debug=True)