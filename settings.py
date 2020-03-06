from flask import Flask
from configparser import ConfigParser
import os

app = Flask(__name__)

parser = ConfigParser()
config_path = r'{0}'.format(os.path.abspath('config.ini'))
parser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))


class Config:
    file_path = os.path.abspath(os.getcwd()) + parser.get('default', 'file_path')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
    SQLALCHEMY_TRACK_MODIFICATIONS = parser.get('default', 'SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_SECRET_KEY = parser.get('default', 'jwt_secret')
