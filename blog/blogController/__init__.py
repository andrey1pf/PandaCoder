import os
import secrets
import threading
import atexit

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()
manager = LoginManager(app)

from blogController import models, routes, parsing


def create_app():

    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global commonDataStruct
        global yourThread
        with dataLock:
            parsing.parsing_news_BBC()
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    def doStuffStart():
        global yourThread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    doStuffStart()
    atexit.register(interrupt)
    return app


app = create_app()
