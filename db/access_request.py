from db.user_db import *
from settings import *
from logger.warning_log import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class AccessToken(db.Model):
    __tablename__ = 'Access Request'
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, unique=False)
    timestamp = db.Column(db.String(100))

    @staticmethod
    def check_user(_login, _password):
        """Check if center exists

        :param _login: login of center
        :param _password: password of center
        :return: boolean
        """
        user = User.query.filter_by(login=_login).first()
        if user is None:
            warning_log('Center is not defined')
            return False
        else:
            return True

    @staticmethod
    def get_all_request():
        """Getting all requests with token

        :return: all token requests
        """
        return [AccessToken.json(access) for access in AccessToken.query.all()]

    def json(self):
        """Represent requests with token by json

        :return: representation of requests
        """
        return {'center_id': self.center_id, 'date': self.timestamp}

    @staticmethod
    def add_request(_center_id, _timestamp):
        """Adding center with new time

        :param _center_id: id of some center
        :param _timestamp: time when this center get token
        :return: nothing
        """
        new_request = AccessToken(center_id=_center_id, timestamp=_timestamp)
        db.session.add(new_request)
        db.session.commit()
