from json import dumps

from sqlalchemy.orm import backref

from db.user_db import *


db = SQLAlchemy(app)


class Animal(db.Model):
    __tablename__ = 'Animals'
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(100))
    age = db.Column(db.Integer, nullable=False)
    species = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer)
    user = db.relationship("User", backref=backref("users", uselist=False))

    @staticmethod
    def add_animal(_center_id, _name, _description, _age, _species, _price):
        new_animal = Animal(center_id=_center_id, name=_name,
                            description=_description, age=_age,
                            species=_species, price=_price)
        db.session.add(new_animal)
        db.session.commit()

    @staticmethod
    def get_all_animal():
        return Animal.query.all()

    def __repr__(self):
        animal_object = {
            'Id': self.center_id,
            'Name': self.name,
            'Description': self.description,
            'Age': self.age,
            'Species': self.species,
            'Price': self.price
        }
        return dumps(animal_object)
