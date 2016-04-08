from flask import Blueprint, render_template
from flask.ext.login import current_user


# Define the blueprint: 'app'
mod_app = Blueprint('app', __name__)

# Set the route and accepted methods
@mod_app.route('/')
@mod_app.route('/index')
def index():
	if current_user.is_authenticated:
		return render_template('dashboard/dashboard.html', title='Your Dashboard')
	else:
		return render_template('index.html', title='Welcome to Hydrobase')
