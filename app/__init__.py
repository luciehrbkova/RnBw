from flask import Flask
from config import Config
# config is the name of config.py module & Config is the name of actual class

app = Flask(__name__)
app.config.from_object(Config)

from app import routes