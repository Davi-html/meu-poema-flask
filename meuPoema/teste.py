from meuPoema import app
from meuPoema import database

with app.app_context():
    database.drop_all()
    database.create_all()