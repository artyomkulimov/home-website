from datetime import datetime
import secrets
from flask import app
from flask_login.utils import _secret_key
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref
from website import db, login_manager, app
from flask_login import UserMixin
#creates tables in the database

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),nullable = False,unique = True)
    email = db.Column(db.String(30),nullable = False,unique = True)
    password = db.Column(db.String(20),nullable = False)
    pfp = db.Column(db.String(100),nullable = False, default = 'default.png')
    posts = db.relationship("Post",backref = "author", lazy = True)
    def get_reset_token(self,expires_sec = 300):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id":self.id}).decode("UTF-8")

class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(50),nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text,nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable = False)

    

