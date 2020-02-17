from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.config import Config

db = SQLAlchemy()
mail = Mail()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    from app.routes.user import account
    from app.routes.post import post_api
    from app.routes.comment import comment_api
    from app.routes.notification import notification_api

    app.register_blueprint(account)
    app.register_blueprint(post_api)
    app.register_blueprint(comment_api)
    app.register_blueprint(notification_api)

    return app
