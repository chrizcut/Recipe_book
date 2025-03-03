from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager


app = Flask(__name__)
login = LoginManager(app)
app.config.from_object(Config)
csrf = CSRFProtect(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
