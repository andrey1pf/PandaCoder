import os
import secrets

from flask import Flask

app = Flask(__name__)

secret_key = secrets.token_urlsafe(32)
app.config.update(
    DEBUG=True,
    SECRET_KEY=secret_key,
    ELASTICSEARCH_URL=os.environ.get('ELASTICSEARCH_URL')
)

from parserController.Parsers import parser_api
from parserController import add_image
