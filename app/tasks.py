# -*- coding:utf-8 -*-
from app.extensions import celery

@celery.task()
def log(msg):
    return msg