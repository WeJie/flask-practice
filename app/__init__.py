# -*- coding:utf-8 -*-

from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_mail import Mail 
from flask_moment import Moment 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_openid import OpenID
from flask_oauth import OAuth

from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
oid = OpenID()
oauth = OAuth()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    oid.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
