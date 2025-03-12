from flask import Flask
from flask_avatars import Avatars
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
avatars = Avatars(app)

app.config['SECRET_KEY'] = '21737b39a5ceb6794d89e31a745de937'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(app)

from meuPoema import routes