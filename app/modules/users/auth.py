import datetime
from flask import request, jsonify
from flask_restx import Resource, Namespace, abort, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.exceptions import BadRequest
from email_validator import validate_email, EmailNotValidError
from .models import User
from .schemas import user_schema, BaseUserSchema
from app import db, jwt
from app.miscellaneous.mixins import AttrDict
from app.miscellaneous.exceptions import (
    InternalServerError,
    SchemaValidationError,
    UserAlreadyExistsError,
    UnauthorizedError,
    UserDoesNotExistError
)
from http import HTTPStatus

api = Namespace('auth', description="Auth")


@api.route('/registration')
class SignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, location='json', help='Username required')
    parser.add_argument('email', type=str, required=True, location='json', help='Email required')
    parser.add_argument('password', type=str, required=True, location='json', help='Password required')
    parser.add_argument('first_name', type=str, location='json', required=False)
    parser.add_argument('last_name', type=str, location='json', required=False)

    @api.response(code=200, description='User created')
    @api.response(code=409, description='User already exists')
    @api.response(code=422, description='Username, password or email are missing')
    @api.expect(parser)
    @api.expect(user_schema)
    def post(self):
        if not request.is_json:
            raise BadRequest
        try:
            body = self.parser.parse_args()
            body['email'] = validate_email(body['email']).email
            user = User(**body)
            db.session.add(user)
            db.session.commit()
            return jsonify(jsonify({"message": "User registered successfully"}))
        except EmailNotValidError:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Invalid email address')
        except IntegrityError:
            raise UserAlreadyExistsError
        except (TypeError, ValueError, KeyError):
            raise SchemaValidationError
        except Exception:
            raise InternalServerError


@api.route('/login')
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, location='json')
    parser.add_argument('password', type=str, required=True, location='json')

    @api.response(code=200, description='User successfully logged in')
    @api.response(code=401, description='User failed to log in')
    @api.expect(parser)
    def post(self):
        if not request.is_json:
            raise BadRequest
        try:
            body = AttrDict(self.parser.parse_args())
            user = User.query.filter_by(username=body.username).one()
            assert user.check_password(body.password)

            expires_in = datetime.timedelta(hours=1)
            access_token = create_access_token(identity=str(user.id),
                                               expires_delta=expires_in,
                                               additional_claims={"role": int(user.role)})
            refresh_token = create_refresh_token(identity=str(user.id))
            response = jsonify(
                access_token=access_token,
                token_type='Bearer',
                refresh_token=refresh_token,
                expires_in=int(expires_in.total_seconds())
            )
            response.status_code = 200
            return response
        except NoResultFound:
            raise UserDoesNotExistError
        except Exception:
            raise UnauthorizedError


@api.route('/refresh')
class Refresh(Resource):

    @jwt.expired_token_loader
    @jwt_required(refresh=True)
    @api.response(code=200, description='Login successful')
    @api.response(code=401, description='Not permitted')
    def get(self):
        # Expired auth header
        user_id = get_jwt_identity()
        expires_in = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=str(user_id), expires_delta=expires_in)
        response = jsonify(
            access_token=access_token,
            token_type='Bearer',
            expires_in=int(expires_in.total_seconds())
        )
        response.status_code = 200
        return response


@api.route('/logout')
class Logout(Resource):

    @jwt_required()
    def delete(self):
        response = jsonify({"message": "Logout successfull"})
        response.status_code = 200

        return response
