from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError


class InternalServerError(InternalServerError):
    description = 'Something went wrong'


class SchemaValidationError(BadRequest):
    description = 'Request is missing required fields'


class UserAlreadyExistsError(BadRequest):
    description = 'User with given email or username already exists'


class UserDoesNotExistError(Unauthorized):
    description = 'User does not exist'


class UnauthorizedError(Unauthorized):
    description = 'Invalid username or password'


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UserDoesNotExist": {
        "message": "User does not exist",
        "status": 401
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    }
}
