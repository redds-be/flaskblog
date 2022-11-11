#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Init file for the flaskblog package
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message = 'You need to be logged in to access this page.'
login_manager.login_message_category = "info"
login_manager.login_view = 'users.login'

mail = Mail()


def create_app(config_class=Config):  # pylint: disable=unused-arguments
    """ Function used for creating a flask app instance """
    app = Flask(__name__, template_folder='./templates')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users  # pylint: disable=import-outside-toplevel
    from flaskblog.posts.routes import posts  # pylint: disable=import-outside-toplevel
    from flaskblog.main.routes import main  # pylint: disable=import-outside-toplevel
    from flaskblog.errors.handlers import errors  # pylint: disable=import-outside-toplevel
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
