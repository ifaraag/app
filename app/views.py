from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import current_user
from app import db

# Define the blueprint: 'app'
mod_app = Blueprint('app', __name__)

# Set the route and accepted methods
@mod_app.route('/')
@mod_app.route('/index')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard.dashboard'))
	else:
		return render_template('index.html')
