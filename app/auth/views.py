from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.ext.login import login_required, login_user, logout_user
from werkzeug import check_password_hash, generate_password_hash

from app import db, login_manager, pubnub, app, _callback
from .models import User
from .forms import LoginForm, SignupForm

mod_auth = Blueprint('auth', __name__)

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    print(request.method)
    if request.method == 'POST':
        user = db.users.find_one({'username': request.form['username']})
        if not user:
            error = 'User does not exist'
        elif not check_password_hash(user['password'], request.form['password']):
            error = 'Invalid credentials. Please try again.'
        else:
            user_obj = User(user['username'])
            login_user(user_obj)
            return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/login.html',
                           title='Log In to Hydrobase',
                           form=form,
                           error=error)

@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    error = None
    if request.method == 'POST':
        existing_user = db.users.find_one({'username' :
                                           request.form['username']})
        if existing_user:
            error = 'Username already exists'
        else:
            new_user = {'username' : request.form['username'],
                        'email' : request.form['email'],
                        'zip' : request.form['zip'],
                        'password' : generate_password_hash(request.form['password'])}
            db.users.insert_one(new_user)
            user = db.users.find_one({'username': request.form['username']})
            pubnub.channel_group_add_channel(channel_group=app.config['PUBNUB_CHANNEL_GRP'], channel=user['username'])
            pubnub.grant(channel=user['username'], auth_key=app.config['PUBNUB_AUTH_KEY'], read=True, write=True, manage=True, ttl=0)
            return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/signup.html', form=form,
                           title='Sign Up for Hydrobase', error=error)

# @mod_auth.route('/googlelogin', methods=['GET', 'POST'])

@mod_auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')

@login_manager.unauthorized_handler
def unauthorized_callback():
  return redirect('/login')

@login_manager.user_loader
def load_user(username):
  u = db.users.find_one({'username': username})
  if not u:
      return None
  return User(u['username'])

def callback(message, channel):
  db.data.insert_one(message)

def error(message):
  db.data.insert_one(message)
