from src import app
from flask import url_for
from flask import Flask, Blueprint
import flask_restplus as restplus

import os
import unittest
import json
import requests

TXT_SUCCESS = 'success'
TXT_FAILURE = 'failure'
URL_ERROR   = 'http://spark-down/'

class EdmRestApiTest(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    app_config = None
    api_prefix = None

    # executed prior to each test
    def setUp(self):
        tapp = Flask(__name__)

        app.initialize_app(tapp)
        tapp.config['TESTING'] = True
        tapp.config['WTF_CSRF_ENABLED'] = False
        tapp.config['DEBUG'] = False
        self.api_prefix = tapp.config['API_PREFIX']

        self.app = tapp.test_client()
        self.assertEquals(tapp.debug, False)
        self.app_config = tapp.config

    # executed after each test
    def tearDown(self):
        pass

        ##########################
        #### Happy path tests ####
        ##########################

    def test_01_get_environment(self):
        url = self.api_prefix+'/environment'
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_02_get_healthcheck(self):

        try:
            url = self.app_config['SPARK_MASTER_URL']
            r = requests.get(url)
            expected_response = 200
            expected_response_status = TXT_SUCCESS

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            expected_response = 200
            expected_response_status = TXT_FAILURE

        url = self.api_prefix+'/healthcheck'
        response = self.app.get(url, follow_redirects=True)
        rdata = json.loads(response.data)
        self.assertEqual(response.status_code, expected_response)
        self.assertEqual(rdata["status"], expected_response_status)

    #########################
    #### Exception tests ####
    #########################

    def test_51_get_environment_exception(self):
        self.app_config['SPARK_MASTER_URL'] = URL_ERROR
        url = self.api_prefix+'/environment'
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_52_get_healthcheck_exception(self):
        self.app_config['SPARK_MASTER_URL'] = URL_ERROR
        url = self.api_prefix+'/healthcheck'
        response = self.app.get(url, follow_redirects=True)
        rdata = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rdata["status"], TXT_FAILURE)


if __name__ == '__main__':
    unittest.main()
