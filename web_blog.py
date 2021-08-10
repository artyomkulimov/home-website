from flask import Flask,render_template,url_for
from forms import RegistrationForm
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ['flask_secret_key']

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/updates")
def updates():
    return render_template("updates.html")
##############################################
@app.route("/register")
def register():
    return render_template("register.html")



if __name__ == "__main__": 
    app.run(debug=True)