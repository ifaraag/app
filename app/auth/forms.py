from flask.ext.wtf import Form
# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, BooleanField, TextField, PasswordField
# Import Form validators
from wtforms.validators import DataRequired, Required, Email, EqualTo


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()]) # Why are we using this?
    remember_me = BooleanField('remember_me', default=False)
    username = TextField('username', [Email(), Required(message='Forgot your email address?')])
    password = PasswordField('password', [Required(message='Must provide a password. ;-)')])