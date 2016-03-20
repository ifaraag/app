from flask import Blueprint, render_template
from app import db, login_manager, pubnub
from flask.ext.login import login_required

mod_devices = Blueprint('devices', __name__)

@mod_devices.route('/devices', methods=['GET'])
@login_required
def list_devices():
	return render_template('devices/device.html',
                           title='Your Devices')

@mod_devices.route('/add_device', methods=['POST'])
@login_required
def add_device():
	pass

@mod_devices.route('/modify_device', methods=['POST'])
@login_required
def modify_device():
	pass

@mod_devices.route('/delete_device', methods=['POST'])
@login_required
def delete_device():
	pass
