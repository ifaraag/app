from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField
from wtforms.validators import Required, Email


class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)
    username = TextField('username')
    password = PasswordField('password')
