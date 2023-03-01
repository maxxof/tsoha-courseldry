import secrets
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    print(user)
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    try:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    except:
        return

def signup(username, password):
    if not bool(username and not username.isspace()) or not bool(password and not password.isspace()):
        return False
    if len(username) < 3 or len(password) < 3:
        return False
    hash_value = generate_password_hash(password)
    try: 
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def username():
    return session.get("username")