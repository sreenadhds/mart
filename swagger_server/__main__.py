#!/usr/bin/env python

import connexion
import logging
from swagger_server import encoder
from swagger_server.models import orm
from swagger_server import globals
logger = logging.getLogger('connexion.apis.flask_api')



def initialise_db(app):
    global  db_session
    globals.db_session=orm.init_db('mysql://root:root@localhost/dreamteam_db')

def init_logging(logger):
    """Initialize application logging."""
    # Initialize flask logging
    log_handler=logging.basicConfig(filename='/tmp/redmart.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logger.addHandler(log_handler)

def main():
    app = connexion.App(__name__, specification_dir='./swagger/',debug=True)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'User Management Service'})
    logger = logging.getLogger(__name__)
    init_logging(logger)
    initialise_db(app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
