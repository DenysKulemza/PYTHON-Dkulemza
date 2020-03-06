from flask_sqlalchemy import SQLAlchemy
from settings import *
from validation.getters import *
from logger.logging import *

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30),  nullable=False)
    password = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(40), nullable=False)

    @staticmethod
    def add_user(request, _login, _password, _address):
        """Adding some user

        :param request: of the input form
        :param _login: login of some center
        :param _password: password of some center
        :param _address: address of some center
        :return: nothing
        """

        new_user = User(login=_login, password=_password, address=_address)
        db.session.add(new_user)
        db.session.commit()
        loggers(request, new_user.id, 'New center was added', new_user.id)

    def display_centers(self):
        """Display centers with id

        :return: name of centers and id
        """
        return {'Name: ': self.login, 'Id: ': str(self.id)}

    @staticmethod
    def get_all_centers():
        """Getting all centers

        :return: centers
        """
        return [User.display_centers(user) for user in User.query.all()]


