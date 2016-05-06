from flask import Blueprint, render_template, Response
from flask.ext.login import login_required, current_user
from app import db
import json

# Define the blueprint: 'documentation'
mod_documentation = Blueprint('documentation', __name__)

@mod_documentation.route('/documentation')
@login_required
def documentation():
	username = current_user.get_id()
	grows_list = []
	grows = db.grows.find({'username' : current_user.get_id()})
	for grow in grows:
		grows_list.append((grow['grow_name'], grow['device_name'], grow['sensors'], grow['actuators']))
	
	return render_template('documentation/documentation.html', username=username, my_grows=grows_list)