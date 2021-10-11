from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from app import modules, miscellaneous
from app.miscellaneous.extensions.admin import Admin
from config import config


blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='JustClassics', version='2', description='Justclassics API')
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
admin = Admin(name='JustClassics', base_template='admin_master.html', template_mode='bootstrap4')
login_manager = LoginManager()
spec = APISpec(
    title="JustClassics",
    version="2",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


def create_app(config_name='development'):
    """For to use dynamic environment"""
    app = Flask(__name__, template_folder='miscellaneous/templates')
    app.config.from_object(config[config_name])

    version = '2'
    app.register_blueprint(blueprint, url_prefix=f'/api/v{version}')

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    cors.init_app(app)
    jwt.init_app(app)

    admin.init_app(app)
    login_manager.init_app(app)
    Swagger(app)

    miscellaneous.init_app(app)
    modules.init_app(app)

    return app


