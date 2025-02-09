import datetime
import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE_CONNECT_OPTIONS = {}

    db_user = os.environ.get('DB_ENV_USER')
    db_pass = os.environ.get('DB_ENV_PASS')
    db_host = os.environ.get('DB_ENV_HOST')
    db_name = os.environ.get('DB_ENV_NAME')

    ENABLED_MODULES = ('users', )

    # Turn off Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    WTF_CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY')

    JWT_SECRET_KEY = 'secret'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_CSRF_CHECK_FORM = True
    #JWT_TOKEN_LOCATION = ['cookies']
    #JWT_COOKIE_SECURE = False
    #JWT_COOKIE_CSRF_PROTECT = True

    # Secret key for signing cookies
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET'

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    JWT_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    """Statement for enabling the development environment"""
    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = f'postgresql://{Config.db_user}:{Config.db_pass}@{Config.db_host}:5432/{Config.db_name}'
    DEBUG = True


class APIConfig(Config):
    """Statement for enabling the api environment"""
    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'api': APIConfig,
}