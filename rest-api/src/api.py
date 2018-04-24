import json

from flask_restplus import Resource, Api
import settings

from flask import Blueprint

from bs4 import BeautifulSoup
import requests

API_PREFIX = settings.API_PREFIX
API_HEALTHCHECK = settings.API_HEALTHCHECK
API_ENVIRONMENT = settings.API_ENVIRONMENT

def add_api(app):
    api = Api(app)
    @api.route(API_HEALTHCHECK)
    class HealthCheck(Resource):
        def get(self):  # pragma: no cover
            try:
                r = requests.get(app.config['SPARK_MASTER_URL'])
                soup = BeautifulSoup(r.content, 'html.parser')
                listItems = soup.find_all('li')
                statusItems = [item.text for item in listItems if 'Status:' in str(item)]
                alive = True if sum(1 for item in statusItems if 'ALIVE' in str(item)) > 0 else False
                statusString = 'success' if alive == True else 'failed'
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                alive = False
                statusString = str(e)
                statusString = 'failed'
            response = {
                "status": statusString,
                "alive": alive}

            print json.dumps(response)
            return response


    @api.route(API_ENVIRONMENT)
    class Environment(Resource):
        def get(self):  # pragma: no cover
            try:
                r = requests.get(app.config['SPARK_MASTER_URL'])
                soup = BeautifulSoup(r.content, 'html.parser')
                listItems = soup.find_all('li')
                spark = {'_'.join(k.lower().split()): " ".join(v.split()) for k, v in
                         (item.text.replace('\n', '').split(':', 1) for item in listItems)}
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                spark = {'error': str(e)}

            return {
                'spark': spark,
                'maintainer': 'Nikolaos Stavros Gavalas (ns.gavalas@gmail.com)',
                'git_repo': 'https://github.com/elastest/elastest-bigdata-service',
            }

    @api.errorhandler
    def default_error_handler(e):  # pragma: no cover
        message = 'An unhandled exception occurred.'
        # log.exception(message)

        if not settings.FLASK_DEBUG:
            return {'message': message}, 500

    return app

