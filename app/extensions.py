# -*- coding:utf-8 -*-
import os

from flask_bootstrap import Bootstrap
from flask_celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, current_user
from flask_mail import Mail 
from flask_moment import Moment 
from flask_oauth import OAuth
from flask_openid import OpenID
from flask_pagedown import PageDown
from flask_principal import Principal, Permission, RoleNeed, UserNeed, \
    identity_loaded
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy 


bootstrap = Bootstrap()
celery = Celery()
db = SQLAlchemy()
debug_toolbar = DebugToolbarExtension()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
oauth = OAuth()
oid = OpenID()
pagedown = PageDown()
principals = Principal()
rest_api = Api()


twitter = oauth.remote_app(
    'twitter',
    base_url='api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    consumer_key= os.getenv('twitter_key') or '',
    consumer_secret= os.getenv('twitter_secret_key') or ''
)
    
@twitter.tokengetter
def get_twitter_oauth_token():
    return session.get('twitter_oauth_token')
