from db.settings import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class DBTest(db.Model):
    __tablename__ = 'dbtest'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String(10))

