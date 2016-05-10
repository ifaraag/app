import flask
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
	seed_data = []
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
	for grow in grows:
		pH_list =[]
		lux_list = []
		EC_list =[]
		TDS_list =[]
		PS_list =[]
		humidity_list = []
		airTemp_list = []
		waterTemp_list =[]
		data_points = db.display.find({'grow_name' : grow['grow_name']}).sort('_id', -1).limit(10);
		print data_points.count()
		for data_point in data_points:
			print data_point['pH']
			pH_list.append(data_point['pH'])
			lux_list.append(data_point['lux'])
			EC_list.append(data_point['EC'])
			TDS_list.append(data_point['TDS'])
			PS_list.append(data_point['PS'])
			humidity_list.append(data_point['humidity'])
			airTemp_list.append(data_point['airTemp'])
			waterTemp_list.append(data_point['waterTemp'])
		pH_list.reverse()
		lux_list.reverse()
		EC_list.reverse()
		TDS_list.reverse()
		PS_list.reverse()
		humidity_list.reverse()
		airTemp_list.reverse()
		waterTemp_list.reverse()
		seed_data.append({"grow_name": grow['grow_name'], "pH" :pH_list, "lux" :lux_list, "EC" :EC_list, \
				"TDS" :TDS_list, "PS" : PS_list, "humidity": humidity_list, "airTemp" : airTemp_list,\
				 "waterTemp": waterTemp_list})

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
			data_point.pop('_id', None)
			concatenated_data.setdefault(grow['grow_name'], []).append(data_point)

	return flask.jsonify(**concatenated_data)