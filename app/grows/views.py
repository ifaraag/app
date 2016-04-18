from flask import Blueprint, render_template, request, url_for, redirect
from app import db, login_manager, pubnub
from flask.ext.login import login_required, current_user

mod_grows = Blueprint('grows', __name__)

@mod_grows.route('/grows/<current_grow>', methods=['GET'])
@login_required
def list_grow(current_grow):
	user_devices = []
	user_grows = []
	device_list = []
	grows_list = []
	assoc_device_name = ''
	username = current_user.get_id()
	grows = db.grows.find({'grow_name' : current_grow})
	for grow in grows:
		assoc_device_name = grow['device_name']
		grows_list.append((current_grow, grow['device_name'], grow['sensors'], grow['actuators']))
	devices = db.devices.find({'device_name': assoc_device_name })
	for device in devices:
		device_list.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit'], device['device_id']))

	devices = db.devices.find({'username': current_user.get_id()})
	for device in devices:
		user_devices.append((device['device_name'], device['type'], \
				device['sensors'], device['actuators'], device['kit'], device['device_id']))
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		user_grows.append((grow['grow_name'], grow['device_name'], grow['sensors'], grow['actuators']))
	
	return render_template('grows/grows.html',
                       		username=username, current_grow=current_grow, current_device=assoc_device_name, \
                           device=device_list, grow=grows_list, my_devices=user_devices, my_grows=user_grows)

@mod_grows.route('/link/<current_grow>/<link_device>', methods=['POST'])
@login_required
def link(current_grow, link_device):
	devices = db.devices.find({'device_name':link_device})
	for device in devices:
		device_id = device['device_id']
	result = db.grows.update_one(
      { "grow_name" : current_grow},
      {
      '$set': {'device_name' : link_device, 'device_id' : device_id, 'sensors':[], 'actuators' : {}}
      },
      upsert=True
      )
	return redirect(url_for('grows.list_grow', current_grow=current_grow))

@mod_grows.route('/edit_grows/<current_grow>', methods=['POST'])
@login_required
def edit_grow(current_grow):
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
	grows = db.grows.find({'grow_name':current_grow})
	for grow in grows:
		device_id = grow['device_id']
	devices = db.devices.find({'device_id':device_id})
	for device in devices:
		act_pins = device['actuators']
	actuators ={}
	for key in act_pins.keys():
		if request.form[key] == "on":
			actuators[key] = act_pins[key]
	grows = db.grows.find({'grow_name':current_grow})
	for grow in grows:
		device_id = device['device_id']
	result = db.grows.update_one(
      { "grow_name" : current_grow},
      {
      '$set': {'sensors':sensors, 'actuators' : actuators}
      },
      upsert=True
      )
	return redirect(url_for('grows.list_grow', current_grow=current_grow))

@mod_grows.route('/add_grows/<grow>/<link_device>', methods=['POST'])
@mod_grows.route('/add_grows/<grow>/<link_device>/<num>', methods=['POST'])
@login_required
def add_grow(grow, link_device, num=1):
	username = current_user.get_id()
	existing_grow = db.grows.find_one({'grow_name' : grow})
	if not existing_grow:
		devices = db.devices.find({'device_name': link_device })
		for device in devices:
			device_id = device['device_id']
		new_grow = {"grow_name" : grow, "device_name" : link_device, "device_id":device_id, \
						"username":username, "sensors":[], "actuators":{}}
		db.grows.insert_one(new_grow)
		return redirect(url_for('grows.list_grow', current_grow=grow))
	else:
		return redirect(url_for('plant_profiles.list_plant_profiles', num=num))



