# codecov ignore

from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from flask_cors import CORS
import logging.config
import settings
from api import add_api

import os
import signal
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer


logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

def configure_app(flask_app):
#    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME

    ebs_port = os.environ.get('EBS_PORT', settings.FLASK_SERVER_PORT)
    ebs_spark_url = os.environ.get('EBS_SPARK_MASTER_URL', settings.SPARK_MASTER_URL)

    flask_app.config['SERVER_HOST'] = settings.FLASK_SERVER_HOST
    flask_app.config['SERVER_PORT'] = ebs_port
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    flask_app.config['SPARK_MASTER_URL'] = ebs_spark_url
    flask_app.config['API_PREFIX'] = settings.API_PREFIX


def initialize_app(flask_app):
    configure_app(flask_app)
    CORS(flask_app)
    add_api(flask_app)

def shutdown_handler(signum=None, frame=None):
    log.info('Shutting down...')
    IOLoop.instance().stop()

def main(): # pragma: no cover
    # app = Flask(__name__)
    # initialize_app(app)
    # logging.config.fileConfig('logging.conf')
    # log = logging.getLogger(__name__)
    # log.info('>>>>> Starting server at http://%s:%d/api/ <<<<<', settings.FLASK_SERVER_HOST, settings.FLASK_SERVER_PORT)
    # app.run(host=settings.FLASK_SERVER_HOST, port=settings.FLASK_SERVER_PORT, debug=settings.FLASK_DEBUG)

    app = Flask(__name__)

    # Tornado implementation
    initialize_app(app)
    # log.info('>>>>> Starting server at http://%s:%d/api/ <<<<<', settings.FLASK_SERVER_HOST, settings.FLASK_SERVER_PORT)

    # app = create_api()
    # check_app = add_check_api()

    ebs_port = os.environ.get('EBS_PORT', 5000)
    ebs_server = HTTPServer(WSGIContainer(app))
    ebs_server.listen(address='0.0.0.0', port=ebs_port)
    # log.info('EBS available at http://{IP}:{PORT}'.format(IP='0.0.0.0', PORT=ebs_port))

    # check_port = os.environ.get('EBS_CHECK_PORT', 5000)
    # check_server = HTTPServer(WSGIContainer(check_app))
    # check_server.listen(address='0.0.0.0', port=check_port)
    log.info('ESM Health available at http://{IP}:{PORT}'.format(IP='0.0.0.0', PORT=ebs_port))

    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig, shutdown_handler)

    log.info('Press CTRL+C to quit.')
    IOLoop.instance().start()

if __name__ == "__main__": # pragma: no cover
    main()



