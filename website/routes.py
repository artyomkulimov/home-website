from flask_login import login_user, current_user, logout_user
from flask_login.utils import login_required
from flask import render_template,url_for,redirect,flash, request
from wtforms.validators import Email
from flask_mail import Message
from website import app, db, bcrypt, mail
from website.models import User, Post
from website.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm, RequestResetForm
from PIL import Image
import secrets
import os


@app.route("/home")
@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html",title = "Home",Header = "Home Page", posts = posts)

@app.route("/credits")
def credits():
    return render_template("credits.html",title = "Credits",Header = "Credits Page")

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
    return render_template("register.html",form = form,title = "Register",Header = "Register")

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
    return render_template("login.html",form = form,title = "Login",Header = "Login")

@app.route("/logout")
def logout():
    logout_user()
    flash(f"You have logged out of your account.","success") 
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



@app.route('/account', methods = ['GET','POST'])
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
        flash(f"You have changed your account's data","success") 
        return redirect(url_for('account'))

    elif request.method == "get":
        form.username.data = current_user.username
        form.email = current_user.email 
    image_file = url_for("static", filename = "pictures/"+ current_user.pfp)
    return render_template("account.html",form = form, image_file = image_file, Header = "Account")

@app.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash(f"Your has been created","success") 
        return redirect(url_for("home")) 
    return render_template("create_post.html", title = "Posts", form = form, header = "User posts")


@app.route("/post/<int:post_id>")
def view_post(post_id):
    post = Post.query.get(post_id)
    return render_template("post.html", title = "Posts", header = "User posts", post = post)

@app.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete(post_id):    
    post = Post.query.get(post_id)
    if current_user.username == post.author.username:
        db.session.delete(post)
        db.session.commit()
        flash(f"Your post has been deleted","success") 
        return redirect(url_for("home")) 

@app.route("/post/<int:post_id>/update", methods = ['GET','POST'])
@login_required
def update(post_id):    
    post = Post.query.get(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f"Your post has been edited","success") 
        return redirect(url_for("view_post", post_id = post_id)) 
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title = "Update Posts",header = "Update Posts", form = form)



@app.route("/user/<string:username>", methods = ['GET','POST'])
def users(username):
    user = User.query.filter_by(username = username).first()
    posts = Post.query.filter_by(author = user)
    return render_template("user_post.html", title = "Update Posts",header = "Update Posts", posts = posts)




def send_reset_email(user):
    token = user.get_reset_token() 
    message = Message("Password Reset Request", sender = "artyomkulimov2@gmail.com", recipients = [user.email])
    message.body = f"To reset your password, click this link: {url_for('reset_request', token = token, _external  = True)}"
    mail.send(message)


@app.route("/reset_password", methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home")) 
    form = RequestResetForm()
    login_form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f"check your mail for a link!","success") 
        return render_template("login.html",form = login_form)
    return render_template("reset_request.html", form = form) # make html


# @app.route("/testing")
# def tesitng():
#     return render_template("trylayout.html",title = "Credits",Header = "Credits Page")