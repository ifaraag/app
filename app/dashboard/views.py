from flask import Blueprint, render_template
from flask.ext.login import login_required, current_user
from app import db

# Define the blueprint: 'dashboard'
mod_dashboard = Blueprint('dashboard', __name__)

@mod_dashboard.route('/dashboard')
@login_required
def dashboard():
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

	return render_template('dashboard/dashboard.html', title='Your Dashboard', username=username, my_devices=device_list, my_grows=grows_list)
