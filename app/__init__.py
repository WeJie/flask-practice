# -*- coding:utf-8 -*-

from flask import Flask 

from config import config
from .controllers.admin import CustomView, CustomModelView
from .extensions import (
    admin, debug_toolbar, bootstrap,
    db, login_manager, current_user,
    mail, moment, oauth,
    oid, pagedown, principals,
    rest_api, Principal, Permission,
    RoleNeed, UserNeed, identity_loaded
)
from .models import Role, Follow, User, Post, Comment, Tag 

login_manager.login_view = 'auth.login'
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"
login_manager.session_protection = 'strong'

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


def create_app(config_name):
    app = Flask(__name__)

    configuration_app(app, config_name)
    configuration_ext(app)
    configuration_blueprint(app)

    @identity_loaded.connect_via(app)
    def on_indetity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user
        
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
                
    return app


def configuration_app(app, config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


def configuration_ext(app):
    admin.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    oid.init_app(app)
    pagedown.init_app(app)
    rest_api.init_app(app)

    admin.add_view(CustomView(name='Custom'))
    models = [Role, Follow, User, Post, Comment, Tag]

    for model in models:
        admin.add_view(
            CustomModelView(model, db.session, category='models')
        )


def configuration_blueprint(app):
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
