# -*- coding:utf-8 -*-

from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, RoleNeed, UserNeed, Permission
from flaskext.markdown import Markdown

from config import config
from .backend.admin import CustomView, CustomModelView
from .extensions import (
    admin, debug_toolbar, bootstrap, db,
    login_manager, mail, moment, oauth, oid,
    principals, rest_api, sentry
)
from .models import Role, User, Post, Comment, Tag

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


def create_app(config_name):
    app = Flask(__name__)

    configuration_app(app, config_name)
    configuration_ext(app)
    configuration_blueprint(app)

    return app


def configuration_app(app, config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


def configuration_ext(app):

    bootstrap.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    oid.init_app(app)
    rest_api.init_app(app)
    sentry.init_app(app)
    Markdown(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please login to access this page."
    login_manager.login_message_category = "info"
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)

    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))
    models = [Role, User, Post, Comment, Tag]
    for model in models:
        admin.add_view(
            CustomModelView(model, db.session, category='models')
        )

    principals.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))


def configuration_blueprint(app):
    from .blog import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

