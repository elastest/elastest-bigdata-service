from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from flask_cors import CORS
import logging.config
import settings
from api import add_api

def configure_app(flask_app):
#    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SERVER_HOST'] = settings.FLASK_SERVER_HOST
    flask_app.config['SERVER_PORT'] = settings.FLASK_SERVER_PORT
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    flask_app.config['SPARK_MASTER_URL'] = settings.SPARK_MASTER_URL
    flask_app.config['API_PREFIX'] = settings.API_PREFIX


def initialize_app(flask_app):
    configure_app(flask_app)
    CORS(flask_app)
    add_api(flask_app)


def main(): # pragma: no cover
    app = Flask(__name__)
    initialize_app(app)
    logging.config.fileConfig('logging.conf')
    log = logging.getLogger(__name__)
    log.info('>>>>> Starting server at http://%s:%d/api/ <<<<<', settings.FLASK_SERVER_HOST, settings.FLASK_SERVER_PORT)
    app.run(host=settings.FLASK_SERVER_HOST, port=settings.FLASK_SERVER_PORT, debug=settings.FLASK_DEBUG)


if __name__ == "__main__": # pragma: no cover
    main()



