#!/usr/bin/env python

import connexion
from  swagger_server.util import get_config
from swagger_server import encoder
from swagger_server.models import orm
from swagger_server import globals
from middlewares import setup_metrics,seed_data
import logging

import os

logger = logging.getLogger('connexion.apis.flask_api')




def initialise_db(app):
    global  db_session
    globals.db_session=orm.init_db('mysql://'+get_config()['db_username']+':'+get_config()['db_password']+'@'+
                                   get_config()['db_host']+'/'+get_config()['db_name'])

def init_logging(logger):
    """Initialize application logging."""
    # Initialize flask logging
    log_handler=logging.basicConfig(filename='/tmp/mart.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logger.addHandler(log_handler)

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'User Management Service'})
    logger = logging.getLogger(__name__)
    init_logging(logger)
    initialise_db(app.app)
    seed_data()
    setup_metrics(app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
