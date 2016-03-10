from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo


class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)
    username = TextField('username')
    password = PasswordField('password')

class SignupForm(Form):
    username = TextField('username', [Required('Please enter a username')])
    email = TextField('email', [Email('Please enter a valid email')])
    password = PasswordField('password', [Required('Please enter a password')])
    confirm = PasswordField('confirm',
                            [EqualTo('password',
                             message='Passwords must match')])
