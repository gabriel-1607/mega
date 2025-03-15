from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/", methods=["POST", "GET"])
def register():
    return render_template("register.html")
