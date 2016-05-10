from flask import Blueprint, render_template, request, url_for, redirect
from app import db, login_manager, pubnub
from flask.ext.login import login_required, current_user

mod_plant_profiles = Blueprint('plant_profiles', __name__)

@mod_plant_profiles.route('/plant_profiles/', methods=['GET'])
@mod_plant_profiles.route('/plant_profiles/<cur>/<first>', methods=['GET'])
# @mod_plant_profiles.route('/plant_profiles/<cur>/<first>/<shift>', methods=['GET'])
@login_required
def list_plant_profiles(cur=1, first=1):
	search = False
	num_profiles = db.plant_profiles.find().count()
	skip = (int(cur)-1) * 8
	lim = 8
	if num_profiles%lim == 0:
		pages = (num_profiles/lim)
	else:
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
	return render_template('plant_profiles/plant_profiles.html', username=username, my_devices=device_list,\
		 my_grows=grows_list, my_plants=plant_list, pages=pages, cur=int(cur), first=int(first), search=search)

@mod_plant_profiles.route('/plant_profiles_next/<cur>/<first>', methods=['GET'])
@login_required
def next_plant_profiles(cur=1, first=1):
	first  = int(first) + 1
	cur = int(cur) + 1
	return redirect(url_for('plant_profiles.list_plant_profiles', cur=cur, first=first))

@mod_plant_profiles.route('/plant_profiles_prev/<cur>/<first>', methods=['GET'])
@login_required
def prev_plant_profiles(cur=1, first=1):
	first  = int(first) - 1
	if int(cur) > first+2:
		cur =  first+2
	return redirect(url_for('plant_profiles.list_plant_profiles', cur=cur, first=first))

@mod_plant_profiles.route('/plant_profiles_first', methods=['GET'])
@login_required
def first_plant_profiles():
	first=1
	cur=1
	return redirect(url_for('plant_profiles.list_plant_profiles', cur=cur, first=first))

@mod_plant_profiles.route('/plant_profiles_last', methods=['GET'])
@login_required
def last_plant_profiles():
	num_profiles = db.plant_profiles.find().count()
	lim = 8
	if num_profiles%lim == 0:
		pages = (num_profiles/lim)
	else:
		pages = (num_profiles/lim)+1
	first=pages-2
	cur=pages
	return redirect(url_for('plant_profiles.list_plant_profiles', cur=cur, first=first))


@mod_plant_profiles.route('/search_plant_profiles', methods=['GET'])
@login_required
def search_plant_profiles(cur=1, first=1, shift="no change"):
	print "here"
	search = True
	num_profiles = db.plant_profiles.find().count()
	skip = (int(cur)-1) * 8
	lim = 8
	if num_profiles%lim == 0:
		pages = (num_profiles/lim)
	else:
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
	print "here1111"
	plants = db.plant_profiles.find({"common_name": request.args.get('search')})
	print "here222"
	for plant in plants:
		plant_list.append(plant)
	return render_template('plant_profiles/plant_profiles.html', username=username, my_devices=device_list,\
		 my_grows=grows_list, my_plants=plant_list, pages=pages, cur=int(cur), first=int(first), search=search)





