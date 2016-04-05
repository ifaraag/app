from flask import Blueprint, render_template, request
from app import db, login_manager, pubnub
from flask.ext.login import login_required, current_user
from app.auth.models import User
import uuid

mod_devices = Blueprint('devices', __name__)

@mod_devices.route('/devices', methods=['GET'])
@login_required
def list_devices():
	device_list = []
	UUID = uuid.uuid4()
	username = current_user.get_id()
	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit']))
	return render_template('devices/devices.html' , title='Your Devices', my_devices=device_list, username=username, uuid=UUID)

@mod_devices.route('/add_device', methods=['POST'])
@login_required
def add_device():
	print(request.form['Lux'])
	print(request.form['Water_Temp'])
	print(request.form['Air_Temp'])
	print(request.form['Humidity'])
	print(request.form['pH'])
	print(request.form['EC'])
	print(request.form['TDS'])
	print(request.form['PS'])
	username = current_user.get_id()
	UUID = uuid.uuid4()
	device_list = []
	existing_device = db.devices.find_one({'device_name' :
                                           request.form['device_name']})
	if not existing_device:
		if request.form['kit'] == "standard":
			new_device = {'username' : username, 'device_name' : request.form['device_name'], 'type' : 'Arduino', 'kit' : request.form['kit'], 'sensors' : ['Lux', 'Water Temperature', 'Air Temperature', 'Humidity', 'pH', 'Electrical Conductivity', 'Total Dissolved Solids', 'Practical Salinity'], 'actuators': {"Light 1" : "30", "Light 2" : "31", "Water Pump" : "32", "Nutrient Pump" : "33", "pH Upper" : "34", "pH Downer" : "35"}}
		else:
			sensors =[]
			if request.form['Lux'] == 'on':
				sensors.append("Lux")
			if request.form['Water_Temp'] == 'on':
				sensors.append("Water Temperature")
			if request.form['Air_Temp'] == 'on':
				sensors.append("Air Temperature")
			if request.form['Humidity'] == 'on':
				sensors.append("Humidity")
			if request.form['pH'] == 'on':
				sensors.append("pH")
			if request.form['EC'] == 'on':
				sensors.append("Electrical Conductivity")
			if request.form['TDS'] == 'on':
				sensors.append("Total Dissolved Solids")
			if request.form['PS'] == 'on':
				sensors.append("Practical Salinity")
			actuators = {}
			if request.form['light_1_pin'] != "":
				actuators['Light 1'] = request.form['light_1_pin']
			if request.form['light_2_pin'] != "":
				actuators['Light 2'] = request.form['light_2_pin']
			if request.form['water_pump_pin'] != "":
				actuators['Water Pump'] = request.form['water_pump_pin']
			if request.form['nutrient_pump_pin'] != "":
				actuators['Nutrient Pump'] = request.form['nutrient_pump_pin']
			if request.form['phUpper_pump_pin'] != "":
				actuators['pH Upper'] = request.form['phUpper_pump_pin']
			if request.form['phDowner_pump_pin'] != "":
				actuators['pH Downer'] = request.form['phDowner_pump_pin']
			new_device = {'username' : username, 'device_name' : request.form['device_name'], 'type' : request.form['device_type'], 'kit' : request.form['kit'], 'sensors' : sensors, 'actuators': actuators}
		db.devices.insert_one(new_device)
	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
	device['sensors'], device['actuators'], device['kit']))
	return render_template('devices/devices.html' , title='Your Devices', \
		my_devices=device_list, username=username, uuid=UUID)

@mod_devices.route('/modify_device', methods=['POST'])
@login_required
def modify_device():
	pass

@mod_devices.route('/delete_device', methods=['POST'])
@login_required
def delete_device():
	pass
