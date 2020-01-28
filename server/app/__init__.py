from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_cors import CORS
import os

from .config import Config

db = SQLAlchemy()
mail = Mail()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    CORS(app)

    # from .routes.testing import api

    # app.register_blueprint(api)

    return app
