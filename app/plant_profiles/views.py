from flask import Blueprint, render_template
from app import db, login_manager, pubnub
from flask.ext.login import login_required, current_user

mod_plant_profiles = Blueprint('plant_profiles', __name__)

@mod_plant_profiles.route('/plant_profiles', methods=['GET'])
@login_required
def list_plant_profiles():
	device_list = []
	grows_list = []
	username = current_user.get_id()
	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit'], device['device_id']))
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		grows_list.append((grow['grow_name'], grow['device_name']))
	return render_template('plant_profiles/plant_profiles.html', username=username, \
	 my_devices=device_list, my_grows=grows_list)