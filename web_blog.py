from flask import Flask,render_template,url_for,redirect,flash
from forms import RegistrationForm,LoginForm
import os
from werkzeug.datastructures import Headers
from flask_sqlalchemy import SQLAlchemy, model

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ['FLASK_SECRET_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),nullable = False)
    email = db.Column(db.String(30),nullable = False)
    password = db.Column(db.String(20),nullable = False)

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
        flash(f"Account was created for user {form.username.data}","success") 
        return redirect(url_for("home"))
    return render_template("register.html",form = form,title = "Register",Header = "This is the registration Form")

@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True: 
            flash(f"You have been logged in to {form.username.data}","success") 
            return redirect(url_for("home"))
        else:
            flash(f"Either username or password incorrect","inv-cred")
    return render_template("login.html",form = form,title = "Login",Header = "This is the Login page")
#################################







if __name__ == "__main__": 
    app.run(debug=True)