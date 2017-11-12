# -*- coding:utf-8 -*-
import os

from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail 
from flask_moment import Moment 
from flask_oauth import OAuth
from flask_openid import OpenID
from flask_principal import Principal
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from raven.contrib.flask import Sentry

admin = Admin()
bootstrap = Bootstrap()
celery = Celery()
db = SQLAlchemy()
debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
oauth = OAuth()
oid = OpenID()
principals = Principal()
rest_api = Api()
sentry = Sentry(dsn='http://80bf021dd8054967a01ea372283f9999:914124d69f18487c888e9f565ce43de7@0.0.0.0:9000/2')


twitter = oauth.remote_app(
    'twitter',
    base_url='api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    consumer_key=os.getenv('twitter_key') or '',
    consumer_secret=os.getenv('twitter_secret_key') or ''
)
