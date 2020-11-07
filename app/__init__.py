from flask import Flask
from config import Config
# config is the name of config.py module & Config is the name of actual class
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#login Manager
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# protecting other pages from unlogged users
login.login_view = 'login'

from app import routes, models