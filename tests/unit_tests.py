import unittest
from db.specie_db import *
from db.animal_db import *
from db.user_db import *
from validation.valid import *


user_true = {
    "Login": "Dandy",
    "Password": 'we',
    'Address': 'sdf'
}
animal_age_true = {
    "Name": "Dingo",
    "Age": "1",
    "Species": "Cat"
}
animal_age_failed = {

    "Name": "Dingo",
    "Age": "-1",
    "Specie": "Cat"

}
user_failed = {
    "Login": "Dandy",
    "password": 'we',
    'Address': 'sdf'
}
specie_exists_now = {
    "Name": "Cat",
    "Description": "red",
    "Prie": "12"
}


class TestProgram(unittest.TestCase):

    def test_invalid_specie_data(self):
        """Test for invalid specie data

        """
        self.assertEqual(False, valid_species(specie_exists_now), 'Test of "invalid data" failed')

    def test_invalid_user(self):
        """Test for invalid user data

        """
        self.assertEqual(False, valid_user(user_failed), 'Test of "invalid user" failed')

    def test_invalid_age(self):
        """Test for incorrect age input

        """
        self.assertEqual(False, valid_animals(animal_age_failed), 'Test of "invalid" failed')

