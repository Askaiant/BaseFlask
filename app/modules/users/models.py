from app import db
from sqlalchemy_utils import types
from app.database.mixins import StandardAttributes
from app.database.roles import UserType


class User(StandardAttributes, db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(types.email.EmailType(length=256), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(length=256), nullable=True)
    last_name = db.Column(db.String(length=256), nullable=True)

    password = db.Column(types.password.PasswordType(max_length=256, schemes=('bcrypt',)), nullable=True)

    role = db.Column(db.Integer, default=UserType.REGULAR_USER.value, server_default='1')
    active = db.Column(db.Boolean, nullable=False, default=False)
    banned = db.Column(db.Boolean, nullable=False, default=False)

    # def __init__(self, username: str, password: str, email: str, first_name: str = '', last_name: str = ''):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     self.first_name = first_name
    #     self.last_name = last_name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def find_admin_with_password(cls, username, password):
        user = cls.query.filter_by(username=username, role=UserType.ADMIN.value).first()
        # fetching only by username and then checking password
        # helps prevent that brute force attacks don't "choke" the server
        # only activate users
        if not user:
            return None
        if not user.active:
            return None
        if user.password == password:
            return user
        return None

    def get_id(self):
        return self.id

    def check_password(self, password):
        return self.password == password

    # @login.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))
