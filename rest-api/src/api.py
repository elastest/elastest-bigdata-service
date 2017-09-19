import logging
import traceback

from flask_restplus import Resource, Api
import settings

from flask import Blueprint

from bs4 import BeautifulSoup
import requests

API_PREFIX = settings.API_PREFIX
API_HEALTHCHECK = '/healthcheck'
API_ENVIRONMENT = '/environment'

log = logging.getLogger(__name__)

blueprint = Blueprint('api', __name__, url_prefix=API_PREFIX)

api = Api(blueprint,
    title='Elastest Bigdata Service API',
    version='1.0',
    description='The REST API for Elastest Bigdata Service component',
)

@api.route(API_HEALTHCHECK)
class HealthCheck(Resource):
    def get(self): # pragma: no cover
        """
        Returns the overall health status of the component.
        """    
        return API_HEALTHCHECK

@api.route(API_ENVIRONMENT)
class Environment(Resource):
    def get(self): # pragma: no cover
        """
        Returns details of the component's environment.
        """    
        return API_ENVIRONMENT

@api.errorhandler
def default_error_handler(e): # pragma: no cover
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


def add_check_api(app):

    from healthcheck import HealthCheck, EnvironmentDump

    health = HealthCheck(app, API_PREFIX + API_HEALTHCHECK, 
                log_on_failure=False, success_ttl=None, failed_ttl=None, failed_status=200)
    envdump = EnvironmentDump(app, API_PREFIX + API_ENVIRONMENT)

    def health_check():

        try:
            r  = requests.get(app.config['SPARK_MASTER_URL'])
            soup = BeautifulSoup(r.content, 'html.parser')
            listItems = soup.find_all('li')
            statusItems = [item.text for item in listItems if 'Status:' in str(item)]
            alive = True if sum(1 for item in statusItems if 'ALIVE' in str(item)) > 0 else False
            statusString = str(statusItems[0])

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            alive = False
            statusString = str(e)

        return alive, statusString


    def application_data():

        try:
            r  = requests.get(app.config['SPARK_MASTER_URL'])
            soup = BeautifulSoup(r.content, 'html.parser')
            listItems = soup.find_all('li')
            spark = {'_'.join(k.lower().split()):" ".join(v.split()) for k,v in (item.text.replace('\n','').split(':',1) for item in listItems) }
            
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            spark = { 'error': str(e) }

        return {
                'spark': spark,
                'maintainer': 'Savas Gioldasis (s.gioldasis@gmail.com)',
                'git_repo': 'https://github.com/elastest/elastest-bigdata-service',
                }

    health.add_check(health_check)
    envdump.add_section("application", application_data)

    return app

def add_api(app):
    add_check_api(app)
    app.register_blueprint(blueprint)
