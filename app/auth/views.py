from flask import Blueprint, render_template, redirect, url_for, \
                                                      request, flash
from .forms import LoginForm

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

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
        return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/login.html',
                         title='Login to Hydrobase',
                         form=form,
                         error=error)