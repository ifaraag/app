from flask import Blueprint, render_template, Response
from flask.ext.login import login_required, current_user
from app import db
import json

# Define the blueprint: 'dashboard'
mod_dashboard = Blueprint('dashboard', __name__)

@mod_dashboard.route('/dashboard')
@login_required
def dashboard():
	device_list = []
	grows_list = []
	range_list = []
	seed_data = {}
	username = current_user.get_id()
	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit'], device['device_id']))
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		grows_list.append((grow['grow_name'], grow['device_name'], grow['sensors'], grow['actuators']))
		ph_min = 0
		ph_max = 0
		ec_min = 0
		ec_max = 0
		for condition_control in grow["controls"]["condition"]:
			if condition_control['actuator'] == 'phUpper_pump':
				ph_min = condition_control['value']
			if condition_control['actuator'] == 'phDowner_pump':
				ph_max = condition_control['value']
			if condition_control['actuator'] == 'nutrient_pump' and condition_control['action'] == 'off':
				ec_max = condition_control['value']
			if condition_control['actuator'] == 'nutrient_pump' and condition_control['action'] == 'on':
				ec_min = condition_control['value']		
		range_list.append({"grow_name": grow['grow_name'], "ph_min" : ph_min, "ph_max": ph_max, "ec_min": ec_min, "ec_max":ec_max})
	grows = db.grows.find({'username' : current_user.get_id()})
	# for grow in grows:
	# 	data_points = db.data.find({'grow_name' : grow['grow_name']}).sort({_id:-1}).limit(10);
	# 	for data_point in data_points:
	# 		seed_data['grow_name']['pH'].append(data_point['pH'])
	# 		seed_data['grow_name']['lux'].append(data_point['lux'])
	# 		seed_data['grow_name']['EC'].append(data_point['EC'])
	# 		seed_data['grow_name']['TDS'].append(data_point['TDS'])
	# 		seed_data['grow_name']['PS'].append(data_point['PS'])
	# 		seed_data['grow_name']['humidity'].append(data_point['humidity'])
	# 		seed_data['grow_name']['airTemp'].append(data_point['airTemp'])
	# 		seed_data['grow_name']['waterTemp'].append(data_point['waterTemp'])

	return render_template('dashboard/dashboard.html', username=username, my_devices=device_list,\
		 my_grows=grows_list, range_list=range_list, seed_data=seed_data)

@mod_dashboard.route('/get_data/', methods = ['GET'])
@login_required
def get_data():
	concatenated_data ={}
	username = current_user.get_id()
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		data_points = db.data.find({'grow_name' : grow['grow_name']})
		for data_point in data_points:
			concatenated_data[grow['grow_name']].append(data_point)
	
	js = json.dumps(concatenated_data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp