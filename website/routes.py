from flask_login import login_user, current_user, logout_user
from flask_login.utils import login_required
from flask import render_template,url_for,redirect,flash, request
from website import app, db, bcrypt
from website.models import User
from website.forms import RegistrationForm,LoginForm,UpdateAccountForm
from PIL import Image
import secrets
import os


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
        user = User(username = form.username.data,email = form.email.data, password = hash_password)
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

def save_picture(picture):
    randomhex = secrets.token_hex(8)
    name, extension = os.path.splitext(picture.filename)
    picture_filename = randomhex+extension
    picture_path = os.path.join("static/pictures", picture_filename)
    print(picture_path)
    output_size = (150,150)
    image = Image.open(picture)
    image.thumbnail(output_size)
    print(picture_path)
    image.save(picture_path)
    return picture_filename



@app.route('/account', methods = ['get','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    print(form.errors)
    if form.validate_on_submit():
        if form.pfp.data:
            file = save_picture(form.pfp.data)
            current_user.pfp = file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))

    elif request.method == "get":
        form.username.data = current_user.username
        form.email = current_user.email 
    image_file = url_for("static", filename = "pictures/"+ current_user.pfp)
    flash(f"You have changed your account's data","success") 
    return render_template("account.html",form = form, image_file = image_file)
