import re
from db.user_db import *


def check_center_id(animal_object):
    if User.get_all_user().__contains__(animal_object['center_id']):
        return True
    else:
        return False


def valid_animals(animal_object):
    if ('Name' in animal_object
            and 'Description' in animal_object
            and age_validation(animal_object)
            and 'Species' in animal_object
            and number_validation(animal_object)):
        return True
    else:
        return False


def valid_user(user_object):
    if ('Login' in user_object
            and 'Password' in user_object
            and 'Address' in user_object):
        return True
    else:
        return False


def valid_species(species_object):
    if ('Name' in species_object
            and 'Description' in species_object
            and number_validation(species_object)):
        return True
    else:
        return False


def number_validation(obj):
    regular_number = re.compile(r'^\d+(?:.\d*)?$')
    if 'Price' in obj and regular_number.match(obj['Price']):
        return True
    else:
        return False


def age_validation(obj):
    regular_number = re.compile(r'^\d+(?:.\d*)?$')
    if 'Age' in obj and regular_number.match(obj['Age']):
        return True
    else:
        return False

