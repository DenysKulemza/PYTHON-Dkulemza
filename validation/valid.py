import re
from db.user_db import *
from jwt import decode
from db.specie_db import *
from logger.warning_log import *


def valid_specie_for_animal(animal_object):
    """Check if specie exists

    :param animal_object: some animal
    :return: boolean
    """
    specie = Specie.query.filter_by(name=animal_object['Species']).first()
    if specie is None:
        warning_log("Specie does not exists. You should add it to database")
        return False
    else:
        return True


def valid_animals(animal_object):
    """Valid animal information

    :param animal_object: some animal
    :return: boolean
    """
    if ('Name' in animal_object
            and age_validation(animal_object)
            and valid_specie_for_animal(animal_object)):
        return True
    else:
        return False


def valid_user(user_object):
    """Valid center information

    :param user_object: some center
    :return: boolean
    """
    if ('Login' in user_object
            and 'Password' in user_object
            and 'Address' in user_object):
        return True
    else:
        warning_log("Register data of center is invalid. Register form should be similar to this:"
                    " {'Login': Login, 'Password': password, 'Address': address")
        return False


def valid_species(species_object):
    """Valid specie information

    :param species_object: some specie
    :return: boolean
    """
    if ('Name' in species_object
            and 'Description' in species_object
            and price_validation(species_object)
            and specie_exists(species_object['Name'])):
        return True
    else:
        return False


def price_validation(obj):
    """Check price for correct input

    :param obj: some object
    :return: boolean
    """
    regular_number = re.compile(r'^\d+(?:.\d*)?$')
    if 'Price' in obj and regular_number.match(obj['Price']):
        return True
    else:
        warning_log(f"The price passed incorrect. Price should be positive number")
        return False


def age_validation(obj):
    """Check age for correct input

    :param obj: some object
    :return: boolean
    """
    regular_number = re.compile(r'^\d+(?:.\d*)?$')
    if 'Age' in obj and regular_number.match(obj['Age']):
        return True
    else:
        warning_log(f"The age passed incorrect. Age should be positive number")
        return False


def center_exists(_login):
    """Check if some center exists

    :param _login: login of some center
    :return: boolean
    """
    center = User.query.filter_by(login=_login).first()
    if center is not None:
        warning_log(f"Center by this login: {_login} is already exists")
        return True
    else:
        return False


def specie_exists(_name):
    """Check if some specie exists

    :param _name: name of some specie
    :return: boolean
    """
    specie = Specie.query.filter_by(name=_name).first()
    if specie is not None:
        warning_log(f"Specie by this name: {_name}  exists")
        return False
    else:
        return True


def check_center_before_delete(_center_id, _id):
    """Check center before delete

        :param _center_id: id of some center
        :param _id: id of some animal
        :return: boolean
        """
    animal = Animal.query.filter_by(id=_id).filter_by(center_id=_center_id).first()
    if animal is not None:
        return True
    else:
        warning_log(f"Center by this id: {_center_id} does not have animal by this id {_id}")
        return False


def valid_token(token, config):
    """Check if token is valid

    :param token: token of center
    :param config: secret config
    :return: if except return boolean
    """
    try:
        decode(token, config)
    except:
        warning_log("Invalid token")
        return True


def valid_login_password(_login, _password):
    """Valid user login and password

    :param _login: login of some center
    :param _password: password of some center
    :return: boolean
    """
    user = User.query.filter_by(login=_login, password=_password).first()
    if user is not None:
        return True
    else:
        return False


def valid_user_login(user):
    """Valid input form 'Login' and 'Password'

    :param user: some user
    :return: boolean
    """
    if ('Login' in user
            and 'Password'in user):
        return True
    else:
        warning_log("Register data of center is invalid. Login form should be similar to this:"
                    " {'Login': login, 'Password': password}")
        return False


def valid_animal_form(animal):
    """Valid input form 'Name', 'Age', 'Species'

    :param animal: some animal
    :return: boolean
    """
    if ('Name' in animal
            and 'Age' in animal
            and 'Species' in animal):
        return True
    else:
        warning_log("Register data of animal are invalid. Input form should be similar to this: "
                    "{'Name': name, 'Age': age, 'Species': specie}")
        return False


def valid_specie_form(specie):
    """Valid input form 'Name', 'Description', 'Price'

    :param specie: some specie
    :return: boolean
    """
    if ('Name' in specie
            and 'Description' in specie
            and 'Price' in specie):
        return True
    else:
        warning_log("Register data of specie are invalid. Input form should be similar to this: "
                    "{'Name': name, 'Description': description, 'Price': price}")
        return False
