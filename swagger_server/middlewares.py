import time

from prometheus_client import Counter, Histogram
from prometheus_client import start_http_server
from flask import request

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