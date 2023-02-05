from flask import Flask
from os import getenv

app = Flask(__name__, static_folder='staticFiles')
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

import routes
