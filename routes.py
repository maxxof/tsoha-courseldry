from app import app
from flask import render_template, request, redirect
import users, reviews
from testcase import data1, data2, data3

@app.route("/", methods=["GET", "POST"])
def index():
    if users.user_id() == 0:
        return redirect("/login")

    posts = reviews.get_reviews()[::-1]
    if request.method == "POST":
        course_filter = request.form["course_filter"]
        filtered = []
        for i in range(len(posts)):
            review = posts[i]
            if course_filter.lower() in review[3].lower():
                filtered.append(review)
        posts = filtered

    return render_template("index.html", posts=posts)

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
        # Following code is made for a test case
        ###
        reviews.post_review(data1)
        reviews.post_review(data2)
        reviews.post_review(data3)
        ###

        return redirect("/")
    else:
        return render_template("error.html", message="choose a valid username and password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new")
def new_review():
    if users.user_id() == 0:
        return redirect("/login")
    return render_template("new.html")

@app.route("/post", methods=["POST"])
def post():
    if users.user_id() == 0:
        return redirect("/login")
    data = {}
    for key in request.form:
        data[key] = request.form[key]
        if key == "course-code":
            continue
        if not check_input(request.form[key]):
            return render_template("error.html", message="Fill the form")

    reviews.post_review(data)
    return redirect("/")

def check_input(input):
    return bool(input and not input.isspace())
