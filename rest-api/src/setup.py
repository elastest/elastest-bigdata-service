# codecov ignore

import os
import inspect
from setuptools import setup, find_packages

NAME = "ebs"
VERSION = "0.1.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools


# XXX update if requirements.txt content is changed
REQUIRES = [
    'aniso8601==1.3.0',
    'astroid==1.5.3',
    'backports.functools-lru-cache==1.4',
    'beautifulsoup4==4.6.0',
    'certifi==2017.7.27.1',
    'chardet==3.0.4',
    'click==6.7',
    'configparser==3.5.0',
    'enum34==1.1.6',
    'Flask==0.12.2',
    'Flask-Cors==3.0.3',
    'flask-restplus==0.10.1',
    'functools32==3.2.3.post2',
    'idna==2.6',
    'isort==4.2.15',
    'itsdangerous==0.24',
    'Jinja2==2.9.6',
    'jsonschema==2.6.0',
    'lazy-object-proxy==1.3.1',
    'MarkupSafe==1.0',
    'mccabe==0.6.1',
    'pbr==3.1.1',
    'pylint==1.7.2',
    'python-dateutil==2.6.1',
    'pytz==2017.2',
    'requests==2.18.4',
    'singledispatch==3.4.0.3',
    'six==1.10.0',
    'stevedore==1.26.0',
    'urllib3==1.22',
    'virtualenv==15.1.0',
    'virtualenv-clone==0.2.6',
    'virtualenvwrapper==4.8.1',
    'Werkzeug==0.12.2',
    'wrapt==1.10.11',
    'tornado',
    'tox'
]

setup(
    name=NAME,
    version=VERSION,
    description="ElasTest Bigdata Service API",
    author_email="elastest-users@googlegroups.com",
    url="https://github.com/elastest/bugtracker",
    keywords=["Swagger", "ElasTest Bigdata Service API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['esm/swagger/swagger.yaml']},
    include_package_data=False,
    long_description="""\
    This is the Elastest Bigdata Service API.
    """
)
