from flask import Blueprint, render_template
from flask.ext.login import current_user
from app import db

# Define the blueprint: 'app'
mod_app = Blueprint('app', __name__)

# Set the route and accepted methods
@mod_app.route('/')
@mod_app.route('/index')
def index():
	device_list = []
	grows_list = []
	username = current_user.get_id()
	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit'], device['device_id']))
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		grows_list.append((grow['grow_name'], grow['device_name'], grow['sensors'], grow['actuators']))
	
	if current_user.is_authenticated:
		return render_template('dashboard/dashboard.html', title='Your Dashboard', username=username, \
			my_devices=device_list, my_grows=grows_list)
	else:
		return render_template('index.html', title='Welcome to Hydrobase')
