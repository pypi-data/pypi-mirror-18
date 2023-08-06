import os

import requests
from celery import Celery

app = Celery('jobqueue', broker=os.environ.get("CELERY_BACKEND",'amqp://guest@localhost//'))

@app.task
def request_get(query):
    return requests.get(query)
