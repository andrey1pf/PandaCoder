import os
import secrets
import threading
import atexit

from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from werkzeug.local import LocalProxy

POOL_TIME = 5

commonDataStruct = {}
dataLock = threading.Lock()
yourThread = threading.Thread()

app = Flask(__name__, template_folder="templates", static_folder="static")
secret_key = secrets.token_urlsafe(32)
app.config.update(
    DEBUG=True,
    SECRET_KEY=secret_key,
    ELASTICSEARCH_URL=os.environ.get('ELASTICSEARCH_URL')
)
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pi31415926@localhost:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

manager = LoginManager(app)

from blogController import models, routes


def create_app():
    return app


app = create_app()
