from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

from db.settings import app
import json

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30),  nullable=False)
    password = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(40), nullable=False)
    animal = db.relationship("User", backref=backref("users", uselist=False))

    @staticmethod
    def add_user(_login, _psswd, _address):
        new_user = User(login=_login, password=_psswd, address=_address)
        db.session.add(new_user)
        db.session.commit()

    def json(self):
        return {'login': self.login, 'password': self.password, 'address': self.address}

    @staticmethod
    def get_all_user():
        return [User.json(user) for user in User.query.all()]

    def __repr__(self):
        user_object = {
            'Id': self.id,
            'Login': self.login,
            'Password': self.password,
            'Address': self.address
        }
        return json.dumps(user_object)
