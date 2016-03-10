from flask import Blueprint, render_template, redirect, url_for, \
                                                      request, flash
from .forms import LoginForm

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from app import login_manager
from flask.ext.login import login_required, login_user, logout_user
from .models import User

# Define the blueprint: 'auth'
mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    print(request.method)
    if request.method == 'POST':
      user = db.users.find_one({'username': request.form['username']})
      if not (user and user['password'] ==  request.form['password']):
        error = 'Invalid credentials. Please try again.'
      else:
        user_obj = User(user['username'])
        login_user(user_obj)
        return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/login.html',
                         title='Log In to Hydrobase',
                         form=form,
                         error=error)

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
  u = db.users.find_one({"username": username})
  if not u:
      return None
  return User(u['username'])
