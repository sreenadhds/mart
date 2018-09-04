import time

from prometheus_client import Counter, Histogram
from prometheus_client import start_http_server
from flask import request
from swagger_server.models import orm
from configs.config import *
from swagger_server import globals
import os
import logging


FLASK_REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Flask Request Latency',
				['method', 'endpoint'])
FLASK_REQUEST_COUNT = Counter('flask_request_count', 'Flask Request Count',
				['method', 'endpoint', 'http_status'])


def before_request():
    request.start_time = time.time()


def after_request(response):
    request_latency = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    FLASK_REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()

    return response
def setup_metrics(app):
    app.before_request(before_request)
    app.after_request(after_request)
    start_http_server(9000)


def seed_data():
    env=os.getenv('FLASK_ENV',"development")
    logging.info(env)
    admin_config=eval(env)
    user = {"dao_username": admin_config['admin_username'], "dao_firstname": "admin",
            "dao_lastname": "admin", "dao_email": "admin@example.com",
            "dao_password": admin_config['admin_hash'], "id": "1000099"}
    try:
        globals.db_session.add(orm.Userinfo(**user))
        globals.db_session.commit()
        logging.info("Admin user initialised")
    except Exception as e:
        logging.error(e)

