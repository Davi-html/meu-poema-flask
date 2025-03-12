from meuPoema import database
from datetime import datetime
import uuid

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(), nullable=False)
    userUnique = database.Column(database.String(), default="@" + str(uuid.uuid4().hex) )
    email = database.Column(database.String(), unique=True, nullable=False)
    password = database.Column(database.String(),nullable=False)
    foto_perfil = database.Column(database.String(), default='default.jpg')
    posts = database.relationship('Post', backref='author', lazy=True)
    bio = database.Column(database.String(), default='Sem biografia')

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(), nullable=False)
    content = database.Column(database.Text(), nullable=False)
    date_posted = database.Column(database.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)