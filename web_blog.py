from flask import Flask,render_template,url_for


app = Flask(__name__)


@app.route("/home")
@app.route("/")
def home():
    return "<h1> default homepage</h1>"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/credits")
def credits():
    return render_template("credits.html")

if __name__ == "__main__":    
    app.run(debug=True) 