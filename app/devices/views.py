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
	username = current_user.get_id()
	UUID = uuid.uuid4()
	device_list = []
	existing_device = db.devices.find_one({'device_name' :
                                           request.form['device_name']})
	if not existing_device:
		new_device = {'username' : username, 'device_name' : request.form['device_name'], \
		'type' : 'Arduino', 'kit' : request.form['kit'], \
		'sensors' : ['Lux', 'Water Temperature', 'Air Temperature', 'Humidity', 'pH', 'Electrical Conductivity', 'Total Dissolved Solids', 'Practical Salinity'], \
        'actuators': {"Light 1" : "30", "Light 2" : "31", "Water Pump" : "32", "Nutrient Pump" : "33", "pH Upper" : "34", "pH Downer" : "35"}
        }
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
