from settings import app, Config
from flask_sqlalchemy import SQLAlchemy

app.config.from_object(Config)
db = SQLAlchemy(app)
