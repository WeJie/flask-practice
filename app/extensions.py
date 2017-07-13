# -*- coding:utf-8 -*-
import os

from app import oauth
from flask_celery import Celery

celery = Celery()

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
