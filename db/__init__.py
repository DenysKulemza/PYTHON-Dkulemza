from settings import *
from flask_sqlalchemy import SQLAlchemy

app.config.from_object(Config)
db = SQLAlchemy(app)
