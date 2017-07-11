# -*- coding:utf-8 -*-

from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_mail import Mail 
from flask_moment import Moment 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, current_user
from flask_pagedown import PageDown
from flask_openid import OpenID
from flask_oauth import OAuth
from flask_principal import Principal, Permission, RoleNeed, identity_loaded
from flask_restful import Api

from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
oid = OpenID()
oauth = OAuth()
rest_api = Api()
principals = Principal()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


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
    rest_api.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    @identity_loaded.connect_via
    def on_indetity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user
        
        if hasattr(current_user, 'id'):
            for role in current_user.roles:
                pass
                
    return app
