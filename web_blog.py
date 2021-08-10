from flask import Flask,render_template,url_for


app = Flask(__name__)


@app.route("/home")
@app.route("/")
def home():
    return render_template("about.html")

# @app.route("/about")
# def about():
    

@app.route("/credits")
def credits():
    return render_template("credits.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/updates")
def updates():
    return render_template("updates.html")

if __name__ == "__main__": 
    app.run(debug=True)