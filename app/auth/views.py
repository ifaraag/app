from flask import Blueprint, render_template, redirect, url_for, request
from .forms import LoginForm

# Define the blueprint: 'auth'
mod_auth = Blueprint('auth', __name__)

# Set the route and accepted methods
@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin' or
            request.form['password'] != 'admin'):
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/login.html',
                           title='Login to Hydrobase',
                           form=form,
                           error=error)
