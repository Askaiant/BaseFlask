from flask import redirect, url_for, request
from flask_admin import expose, helpers, AdminIndexView
import flask_login as login
from wtforms import form, validators, fields
from app import db, admin, login_manager
from app.modules.users.models import User


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_username(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user or password')

    def get_user(self):
        return User.find_admin_with_password(self.username.data, self.password.data)


class CustomAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return self.render('admin/index.html', form=form)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        _form = LoginForm(request.form)
        if helpers.validate_form_on_submit(_form):
            user = _form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = _form
        return self.render('admin/index.html', form=_form)

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


def init_login():
    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))


admin.set_index_view(index_view=CustomAdminIndexView())
init_login()
