from flask_restx import Resource, Namespace
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.miscellaneous.permissions import admin_required
from .schemas import users_schema, user_schema
from .models import User

api = Namespace('users', description="Users")

@api.route('/me')
class Me(Resource):
    """
    Get information of authenticated user.
    """

    @jwt_required()
    def get(self):
        return user_schema.dump(User.query.get(get_jwt_identity()))


@api.route('/users')
class Users(Resource):
    """
    Manipulations with users.
    """

    #@api.response(schemas.BaseUserSchema(many=True), description='List all users')
    @jwt_required()
    @admin_required()
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

