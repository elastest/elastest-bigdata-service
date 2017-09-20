# codecov ignore

from flask import Flask, Blueprint
from api import api
import json
import runebs
import logging.config

fileName = 'api.json'

def main(): # pragma: no cover
    logging.config.fileConfig('logging.conf')
    log = logging.getLogger(__name__)
    app = Flask(__name__)
    runebs.initialize_app(app)
    app.config['SERVER_NAME'] = ''
    with app.app_context():
        api_schema = api.__schema__
        api_schema['basePath'] = api_schema['basePath'].replace('http://', '')
        api_schema['basePath'] = '/' if not api_schema['basePath'] else api_schema['basePath']
        with open(fileName, 'w') as outfile:
            json.dump(api_schema, outfile, indent=4)
    log.info('Exported file ' + fileName + ' ...')

if __name__ == "__main__": # pragma: no cover
    main()




