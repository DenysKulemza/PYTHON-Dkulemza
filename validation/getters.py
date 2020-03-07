from db.specie_db import *
from db.animal_db import *


def get_specie(_name):
    """ Get specie by name

    :param _name: name of specie
    :return: specific specie by name
    """
    return Specie.query.filter_by(name=_name).first()


def get_access():
    """ Return last id by token

    :return: last access id by toke
    """
    return AccessToken.query.order_by(AccessToken.id.desc()).first()


def get_animal_id__by_name_for_logger():
    """Getting animal id by name for logging it

    :return: id of some animal
    """
    animal = Animal.query.order_by(Animal.id.desc()).first()
    return animal.id


def get_specie_by_name_for_logger(_name):
    """Getting specie id by name for logging it

    :param _name: name of some specie
    :return: if of some specie
    """
    specie = Specie.query.order_by(Specie.id.desc()).first()
    return specie.id
