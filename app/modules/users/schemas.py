from app import ma, spec
from .models import User

BASE_USER_FIELDS = (User.id.key, User.email.key, User.username.key)


class BaseUserSchema(ma.Schema):
    """
    Base user schema exposes only the most general fields.
    """

    class Meta:
        model = User
        fields = BASE_USER_FIELDS
        dump_only = (User.id.key,)


user_schema = BaseUserSchema()
users_schema = BaseUserSchema(many=True)

spec.components.schema("BaseUserSchema", schema=BaseUserSchema)

