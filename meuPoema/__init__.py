from flask import Flask
from flask_avatars import Avatars
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
avatars = Avatars(app)

app.config['SECRET_KEY'] = '21737b39a5ceb6794d89e31a745de937'

if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'alert-info'

from meuPoema import routes