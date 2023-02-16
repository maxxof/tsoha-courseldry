from app import app
from flask import render_template, request, redirect
import users, reviews
from testcase import data1, data2, data3

@app.route("/", methods=["GET", "POST"])
def index():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/login")

    posts = reviews.get_reviews()
    user_agreements = reviews.get_user_agreements(user_id)
    user_disagreements = reviews.get_user_disagreements(user_id)

    agreements = [i.review_id for i in user_agreements]
    disagreements = [j.review_id for j in user_disagreements]

    if request.method == "POST":
        course_filter = request.form["course_filter"]
        filtered = []
        for i in range(len(posts)):
            review = posts[i]
            if course_filter.lower() in review[3].lower():
                filtered.append(review)
        posts = filtered[:]

    return render_template("index.html", posts=posts,user_agreements=agreements, user_disagreements=disagreements)

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
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/login")
    
    return render_template("new.html")

@app.route("/post", methods=["POST"])
def post():
    user_id = users.user_id()
    if user_id == 0:
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

@app.route("/agree", methods=["POST"])
def agree():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/login")
    
    review_id = request.form["agree"]
    reviews.agree(review_id, user_id)
    return redirect(request.referrer)

@app.route("/disagree", methods=["POST"])
def disagree():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/login")

    review_id = request.form["disagree"]
    reviews.disagree(review_id, user_id)
    return redirect(request.referrer)

@app.route("/unagree", methods=["POST"])
def unagree():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/login")
    
    review_id = request.form["unagree"]
    reviews.unagree(review_id, user_id)
    return redirect(request.referrer)

@app.route("/undisagree", methods=["POST"])
def undisagree():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/login")
    
    review_id = request.form["undisagree"]
    reviews.undisagree(review_id, user_id)
    return redirect(request.referrer)

def check_input(input):
    return bool(input and not input.isspace())
