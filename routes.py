from app import app
from flask import render_template, request, redirect, session
import users

@app.route("/")
def index():
    if users.user_id() == 0:
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Wrong username or password")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return render_template("error.html", message="Passwords don't match")
    if users.signup(username, password2):
        return redirect("/")
    if not bool(username and not username.isspace()):
        return render_template("error.html", message="username cannot be empty")
    return render_template("error.html", message=f"username {username} is already taken")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
