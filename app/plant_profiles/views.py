from flask import Blueprint, render_template
from app import db, login_manager, pubnub
from flask.ext.login import login_required, current_user

mod_plant_profiles = Blueprint('plant_profiles', __name__)

@mod_plant_profiles.route('/plant_profiles', methods=['GET'])
@mod_plant_profiles.route('/plant_profiles/<num>', methods=['GET'])
@login_required
def list_plant_profiles(num=1):
	num_profiles = 372
	skip = (int(num)-1) * 8
	lim = 8
	pages = (num_profiles/lim)+1
	device_list = []
	grows_list = []
	plant_list =[]
	username = current_user.get_id()
	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit'], device['device_id']))
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		grows_list.append((grow['grow_name'], grow['device_name']))
	plants = db.plant_profiles.find().skip(skip).limit(lim)
	for plant in plants:
		plant_list.append(plant)
	return render_template('plant_profiles/plant_profiles.html', username=username, \
	 my_devices=device_list, my_grows=grows_list, my_plants=plant_list, pages=pages, cur=int(num))