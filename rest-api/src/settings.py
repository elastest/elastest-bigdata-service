# Flask settings
#FLASK_SERVER_NAME = 'localhost'
FLASK_SERVER_HOST = '0.0.0.0'
FLASK_SERVER_PORT = 5000
FLASK_DEBUG = False  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Other settings
SPARK_MASTER_URL = 'http://spark-master:8080/'
API_PREFIX = ''
