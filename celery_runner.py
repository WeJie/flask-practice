# -*- coding:utf-8 -*-
import os

from celery import Celery

from app import create_app
from app.tasks import log
from config import config


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND_URL'],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

env = os.environ.get('WEBAPP_ENV', 'development')
flask_app = create_app(env)

celery = make_celery(flask_app)
