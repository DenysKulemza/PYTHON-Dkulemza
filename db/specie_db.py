from flask_sqlalchemy import SQLAlchemy
from db.settings import app
import json

db = SQLAlchemy(app)


class Specie(db.Model):
    __tablename__ = 'specie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10),  nullable=False)
    description = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @staticmethod
    def add_specie(_name, _description, _price):
        new_specie = Specie(name=_name, description=_description, price=_price)
        db.session.add(new_specie)
        db.session.commit()

    def json(self):
        return {'name': self.name, 'description': self.description, 'price': self.price}

    @staticmethod
    def get_all_specie():
        return [Specie.json(specie) for specie in Specie.query.all()]

    def __repr__(self):
        specie_object = {
            'Id': self.id,
            'Name': self.name,
            'Description': self.description,
            'Price': self.price
        }
        return json.dumps(specie_object)