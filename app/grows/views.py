from flask import Blueprint, render_template
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
		grows_list.append((current_grow, grow['device_name']))
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
		user_grows.append((grow['grow_name'], grow['device_name']))
	
	return render_template('grows/grows.html',
                           title='Your Grows', username=username, current_grow=current_grow, current_device=assoc_device_name, \
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
      '$set': {'device_name' : link_device, 'device_id' : device_id}
      },
      upsert=True
      )
	user_devices = []
	user_grows = []
	device_list = []
	grows_list = []
	assoc_device_name = ''
	username = current_user.get_id()
	grows = db.grows.find({'grow_name' : current_grow})
	for grow in grows:
		assoc_device_name = grow['device_name']
		grows_list.append((current_grow, grow['device_name']))
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
		user_grows.append((grow['grow_name'], grow['device_name']))
	
	return render_template('grows/grows.html',
                           title='Your Grows', username=username, current_grow=current_grow, current_device=assoc_device_name, \
                           device=device_list, grow=grows_list, my_devices=user_devices, my_grows=user_grows)

