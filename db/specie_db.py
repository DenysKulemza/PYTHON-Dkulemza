from db.access_request import *
from settings import *
from logger.logging import *

db = SQLAlchemy(app)


class Specie(db.Model):
    __tablename__ = 'specie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @staticmethod
    def add_specie(request, _name, _description, _price):
        """Adding new specie

        :param request: request of input form
        :param _name: name of some specie
        :param _description: description of some specie
        :param _price: price of some specie
        :return: nothing
        """
        new_specie = Specie(name=_name, description=_description, price=_price)
        db.session.add(new_specie)
        db.session.commit()
        access = AccessToken.query.order_by(AccessToken.id.desc()).first()
        loggers(request, access.center_id, 'New specie was added', new_specie.id)

    def json(self, count):
        """Representation of specie and amount of all specie

        :param count: amount of some specie in centers
        :return: names and amount of all animal
        """
        return {'name': self.name, f'amount of "{self.name}"': count}

    def specie_animals(self, animal_object):
        """Represent species, id, names in json format

        :param animal_object: some animal
        :return: representation of specie
        """
        return {'Animal name ': animal_object, 'Id ': self.id, 'Specie ': self.name}

    @staticmethod
    def get_specie_animals(_id):
        """Getting animal by specie

        :param _id: some id of animal
        :return: animal in json
        """
        return [Specie.find_animal(_id) for _ in Specie.query.all()]

    @staticmethod
    def find_animal(_id):
        """Finds some animal

        :param _id: id of some specie
        :return: animal
        """
        specie = Specie.query.filter_by(id=_id).first()
        return [Specie.specie_animals(specie, animal.name) for animal in Animal.query.filter_by(species=specie.name).all()]
