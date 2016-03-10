from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField
from wtforms.validators import Required, Email


class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)
    username = TextField('username',
                         [Email(), Required(message='Forgot your email address?')])
    password = PasswordField('password',
                             [Required(message='Must provide a password. ;-)')])
