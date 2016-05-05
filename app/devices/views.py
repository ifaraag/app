from flask import Blueprint, render_template, request, url_for, redirect
from app import db, login_manager, pubnub
from flask.ext.login import login_required, current_user
from app.auth.models import User
import uuid

mod_devices = Blueprint('devices', __name__)

@mod_devices.route('/devices', methods=['GET'])
@login_required
def list_devices():
	device_list = []
	grows_list = []
	UUID = str(uuid.uuid4())
	username = current_user.get_id()
	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit'], device['device_id']))
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		grows_list.append((grow['grow_name'], grow['device_name']))
	return render_template('devices/devices.html' , my_devices=device_list, my_grows=grows_list, username=username, uuid=UUID)

@mod_devices.route('/add_device/<new_device_id>', methods=['POST'])
@login_required
def add_device(new_device_id):
	username = current_user.get_id()
	existing_device = db.devices.find_one({'device_name' :
                                           request.form['device_name']})
	if not existing_device:
		if request.form['kit'] == "standard":
			new_device = {'username' : username, 'device_id': new_device_id, 'device_name' : request.form['device_name'], 'type' : 'Arduino', 'kit' : request.form['kit'], \
			'sensors' : ['Lux', 'Water_Temp', 'Air_Temp', 'Humidity', 'pH', 'EC', 'TDS', 'PS'], \
			'actuators': {"light_1" : "30", "light_2" : "31", "water_pump" : "32", "nutrient_pump" : "33", "phUpper_pump" : "34", "phUpper_pump" : "35"}}
		else:
			sensors =[]
			if request.form['Lux'] == 'on':
				sensors.append("Lux")
			if request.form['Water_Temp'] == 'on':
				sensors.append("Water_Temp")
			if request.form['Air_Temp'] == 'on':
				sensors.append("Air_Temp")
			if request.form['Humidity'] == 'on':
				sensors.append("Humidity")
			if request.form['pH'] == 'on':
				sensors.append("pH")
			if request.form['EC'] == 'on':
				sensors.append("EC")
			if request.form['TDS'] == 'on':
				sensors.append("TDS")
			if request.form['PS'] == 'on':
				sensors.append("PS")
			actuators = {}
			if request.form['light_1_pin'] != "":
				actuators['light_1'] = request.form['light_1_pin']
			if request.form['light_2_pin'] != "":
				actuators['light_2'] = request.form['light_2_pin']
			if request.form['water_pump_pin'] != "":
				actuators['water_pump'] = request.form['water_pump_pin']
			if request.form['nutrient_pump_pin'] != "":
				actuators['nutrient_pump'] = request.form['nutrient_pump_pin']
			if request.form['phUpper_pump_pin'] != "":
				actuators['phUpper_pump'] = request.form['phUpper_pump_pin']
			if request.form['phDowner_pump_pin'] != "":
				actuators['phDowner_pump'] = request.form['phDowner_pump_pin']
			new_device = {'username' : username, 'device_id': new_device_id, \
				'device_name' : request.form['device_name'], 'type' : request.form['device_type'], \
					'kit' : request.form['kit'], 'emergency_stop': 'false', 'sensors' : sensors, 'actuators': actuators}
		db.devices.insert_one(new_device)
	return redirect(url_for('devices.list_devices'))

@mod_devices.route('/edit_device/<device_id>', methods=['POST'])
@login_required
def edit_device(device_id):
	sensors =[]
	if request.form['Lux'] == 'on':
		sensors.append("Lux")
	if request.form['Water_Temp'] == 'on':
		sensors.append("Water_Temp")
	if request.form['Air_Temp'] == 'on':
		sensors.append("Air_Temp")
	if request.form['Humidity'] == 'on':
		sensors.append("Humidity")
	if request.form['pH'] == 'on':
		sensors.append("pH")
	if request.form['EC'] == 'on':
		sensors.append("EC")
	if request.form['TDS'] == 'on':
		sensors.append("TDS")
	if request.form['PS'] == 'on':
		sensors.append("PS")
	actuators = {}
	if request.form['light_1_pin'] != "":
		actuators['light_1'] = request.form['light_1_pin']
	if request.form['light_2_pin'] != "":
		actuators['light_2'] = request.form['light_2_pin']
	if request.form['water_pump_pin'] != "":
		actuators['water_pump'] = request.form['water_pump_pin']
	if request.form['nutrient_pump_pin'] != "":
		actuators['nutrient_pump'] = request.form['nutrient_pump_pin']
	if request.form['phUpper_pump_pin'] != "":
		actuators['phUpper_pump'] = request.form['phUpper_pump_pin']
	if request.form['phDowner_pump_pin'] != "":
		actuators['phDowner_pump'] = request.form['phDowner_pump_pin']
	result = db.devices.update_one(
      { "device_id" : device_id },
      {
      '$set': {'device_name': request.form['device_name'], 'sensors' : sensors, 'actuators' : actuators}
      },
      upsert=True
      )

	grows = db.grows.find({'device_id' : device_id})
	for grow in grows:
		g_sensors = grow['sensors']
		g_actuators = grow['actuators']
		g_controls = grow['controls']
		for s in g_sensors:
			if s not in sensors:
				g_sensors.remove(s)
		for key in g_actuators.keys():
			if key not in actuators.keys():
				g_actuators.pop(key, None)
		for time_control in g_controls["time"]:
			if time_control["actuator"] not in actuators.keys():
				g_controls["time"].remove(time_control)
		for condition_control in g_controls["condition"]:
			if condition_control["actuator"] not in actuators.keys() or condition_control["sensor"] not in sensors:
				g_controls["condition"].remove(condition_control)
		result = db.grows.update_one(
	      { "grow_name" : grow['grow_name']},
	      {
	      '$set': {'device_name': request.form['device_name'], 'sensors' : g_sensors, 'actuators' : g_actuators, 'controls': g_controls }
	      },
	      upsert=True
	      )

	return redirect(url_for('devices.list_devices'))

@mod_devices.route('/delete_device/<device_id>', methods=['POST'])
@login_required
def delete_device(device_id):
	username = current_user.get_id()
	result = db.grows.update_many(
      { "device_id" : device_id },
      {
      '$set': {'device_name': "", 'device_id':"", 'sensors' : [], 'actuators' : {}, 'controls':{}}
      },
      upsert=True
      )

	device = db.devices.delete_one({'device_id' : device_id})
	result = db.data.update_many({ "device_id" : device_id},
      {
      '$set': {'device_name' : "", 'device_id' : ""}
      },
      upsert=True
      )
	return redirect(url_for('devices.list_devices'))

@mod_devices.route('/emergency_stop/<device_id>', methods=['POST'])
@login_required
def emergency_stop(device_id):
	
	result = db.grows.update_one(
	      { "device_id" : device_id},
	      {
	      '$set': {'emergency_stop': request.form['emergency_stop_state']}
	      },
	      upsert=True
	      )
	return redirect(url_for('devices.list_devices'))













