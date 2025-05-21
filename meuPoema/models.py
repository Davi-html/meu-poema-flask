from meuPoema import database, login_manager
from datetime import datetime
import uuid
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(), nullable=False)
    userUnique = database.Column(database.String(), default=lambda: "@" + uuid.uuid4().hex[:10])
    email = database.Column(database.String(), unique=True, nullable=False)
    password = database.Column(database.String(),nullable=False)
    foto_perfil = database.Column(database.String(), default='default.jpg')
    posts = database.relationship('Post', backref='author', lazy=True)
    bio = database.Column(database.String(), default='Sem biografia')
    followers = database.Column(database.Integer(), default=0)
    following = database.Column(database.Integer(), default=0)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(), nullable=False)
    content = database.Column(database.Text(), nullable=False)
    date_posted = database.Column(database.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)