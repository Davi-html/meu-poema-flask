from meuPoema import app
from meuPoema import database

with app.app_context():
    database.create_all()