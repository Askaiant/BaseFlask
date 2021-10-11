from flask_admin.contrib.sqla import ModelView
import flask_login as login
from app import db, admin
from app.modules.users.models import User


class UserView(ModelView):
    column_list = ['username', 'first_name', 'last_name', 'email', 'role', 'active', 'banned', 'created', 'updated']
    column_searchable_list = ['username', 'email']
    column_filters = ['active', 'role']
    form_columns = ('username', 'password', 'email', 'first_name', 'last_name', 'role', 'active')

    def is_accessible(self):
        return login.current_user.is_authenticated


admin.add_view(UserView(User, db.session))
