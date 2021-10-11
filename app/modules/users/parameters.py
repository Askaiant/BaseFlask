from flask_marshmallow import base_fields
from app.miscellaneous.parameters import PostJSONParameters
from . import schemas


class RegisterUserParameters(PostJSONParameters, schemas.BaseUserSchema):

    class Meta(schemas.BaseUserSchema.Meta):
        exclude = ('roles', 'active', 'banned',)

    username = base_fields.String(required=True)
    password = base_fields.String(required=True)
    email = base_fields.String(required=True)

    first_name = base_fields.String(required=False)
    last_name = base_fields.String(required=False)
