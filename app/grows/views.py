from flask import Blueprint, render_template, request, url_for, redirect
from app import db, login_manager, pubnub
from flask.ext.login import login_required, current_user
import datetime

mod_grows = Blueprint('grows', __name__)

@mod_grows.route('/grows/<current_grow>', methods=['GET'])
@login_required
def list_grow(current_grow):
    count = 0
    data = {}
    user_devices = []
    user_grows = []
    device_list = []
    grows_list = []
    assoc_device_name = ''
    username = current_user.get_id()
    grows = db.grows.find({'grow_name' : current_grow})
    for grow in grows:
        assoc_device_name = grow['device_name']
        experiment = grow['experiment']
        grows_list.append((current_grow, grow['device_name'], grow['sensors'], grow['actuators'], grow['controls'], grow['plant_profile']))
    data_points = db.data.find({'grow_name' : current_grow}).sort({_id:-1}).limit(151200)
    for datapoint in data_points:
        if count%3600 == 0:
            data['grow_name']['pH'].append(data_point['pH'])
            data['grow_name']['lux'].append(data_point['lux'])
            data['grow_name']['EC'].append(data_point['EC'])
            data['grow_name']['TDS'].append(data_point['TDS'])
            data['grow_name']['PS'].append(data_point['PS'])
            data['grow_name']['humidity'].append(data_point['humidity'])
            data['grow_name']['airTemp'].append(data_point['airTemp'])
            data['grow_name']['waterTemp'].append(data_point['waterTemp'])
        count+=1
    if assoc_device_name == "":
        device_list.append(("No Device Linked", "No Device Linked", [] ,{}, "", ""))
    else:
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
        user_grows.append((grow['grow_name'], grow['device_name'], grow['sensors'], grow['actuators'], grow['controls']))
    
    return render_template('grows/grows.html',
                            username=username, current_grow=current_grow, experiment=experiment, current_device=assoc_device_name, \
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
      '$set': {'device_name' : link_device, 'device_id' : device_id, 'sensors': [], 'actuators' : {}, 'controls' : {"time":[], "condition" :[]} }
      },
      upsert=True
      )
    return redirect(url_for('grows.list_grow', current_grow=current_grow))

@mod_grows.route('/edit_grows/<current_grow>', methods=['POST'])
@login_required
def edit_grow(current_grow):
    grows = db.grows.find({'grow_name':current_grow})
    for grow in grows:
        device_id = grow['device_id']
    devices = db.devices.find({'device_id':device_id})
    for device in devices:
        d_actuators = device['actuators']
        d_sensors = device['sensors']
    sensors =[]
    for sensor in d_sensors:
        if request.form[sensor] == 'on':
            sensors.append(sensor)
    
    actuators ={}
    for key in d_actuators.keys():
        if request.form[key] == "on":
            actuators[key] = d_actuators[key]
    grows = db.grows.find({'grow_name':current_grow})
    for grow in grows:
        device_id = device['device_id']
        g_controls = grow['controls']
        for time_control in g_controls["time"]:
            if time_control["actuator"] not in actuators.keys():
                g_controls["time"].remove(time_control)
        for condition_control in g_controls["condition"]:
            if condition_control["actuator"] not in actuators.keys() or condition_control["sensor"] not in sensors:
                g_controls["condition"].remove(condition_control)
    result = db.grows.update_one(
      { "grow_name" : current_grow},
      {
      '$set': {'sensors':sensors, 'actuators' : actuators, 'controls':g_controls}
      },
      upsert=True
      )
    return redirect(url_for('grows.list_grow', current_grow=current_grow))

@mod_grows.route('/add_custom_grows/<current_grow>', methods=['POST'])
@login_required
def add_custom_grow(current_grow):
    username = current_user.get_id()
    existing_grow = db.grows.find_one({'grow_name' : request.form['new_grow_name']})
    if not existing_grow:
        devices = db.devices.find({'device_name': request.form['device']})
        for device in devices:
            device_id = device['device_id']
            sensors = device['sensors']
            actuators = device['actuators']
        
        new_grow_controls = {"time":[], "condition" : []}
        condition_control_num = 0
        time_control_num = 0
        for key in request.form.keys():
            if key[:-1] == "if_this_condition_":
                condition_control_num+=1
            elif key[:-1] == "time_int_":
                time_control_num+=1
            if time_control_num == 1:
                if request.form['time_int_1'] == "":
                    time_control_num = 0
            if condition_control_num == 1:
                if request.form['if_this_condition_1'] == "":
                    condition_control_num = 0
        
        print time_control_num, actuators.keys()
        for i in range(time_control_num):
            
            print str(request.form['actuator_control_'+str(i+1)+'_actuator'])
            if str(request.form['actuator_control_'+str(i+1)+'_actuator']) in actuators.keys():
                new_grow_controls["time"].append({"action": "toggle",
                "actuator": request.form['actuator_control_'+str(i+1)+'_actuator'],
                "unit": request.form['time_hour_min_'+str(i+1)],
                "value": int(request.form['time_int_'+str(i+1)]),
                "start_date" : request.form['startdate_activity_'+str(i+1)],
                "finish_date" : request.form['finishdate_activity_'+str(i+1)]})
        
        print "here"
        for i in range(condition_control_num):
            if request.form['if_this_condition_'+str(i+1)] in sensors and \
                            request.form['do_this_condition_'+str(i+1)].split("-")[0] in actuators.keys():
                new_grow_controls["condition"].append({"action": (request.form['do_this_condition_'+str(i+1)].split("-")[1]),
                "actuator": request.form['do_this_condition_'+str(i+1)].split("-")[0],
                "sensor" : request.form['if_this_condition_'+str(i+1)],
                "operator" : request.form['is_condition_'+str(i+1)].split("%")[0],
                "unit": request.form['if_this_condition_'+str(i+1)],
                "value": float(request.form['to_this_condition_'+str(i+1)])})

        print "here 22222"
        new_grow = {"grow_name" : request.form['new_grow_name'], "plant_profile": "user defined" , "experiment" :"false", "device_name" : request.form['device'], "device_id":device_id, \
                        "username":username, "sensors":sensors, "actuators":actuators, "controls": new_grow_controls }
        db.grows.insert_one(new_grow)
        return redirect(url_for('grows.list_grow', current_grow=request.form['new_grow_name']))
    else:
        return redirect(url_for('grows.list_grow', current_grow=current_grow))


@mod_grows.route('/add_grows/', methods=['POST'])
@mod_grows.route('/add_grows/<num>', methods=['POST'])
@login_required
def add_grow(num=1):
    username = current_user.get_id()
    existing_grow = db.grows.find_one({'grow_name' : request.form['grow_name']})
    if not existing_grow:
        devices = db.devices.find({'device_name': request.form['device_name']})
        for device in devices:
            device_id = device['device_id']
            sensors = device['sensors']
            actuators = device['actuators']
        plant_profiles = db.plant_profiles.find({"identifier" : request.form['plant_type']})
        for profile in plant_profiles:
            if 'ph_minimum' not in profile.keys():
                ph_min = 6.75
            elif profile['ph_minimum'] is "":
                ph_min = 6.75
            else:
                ph_min = profile['ph_minimum']
            if 'ph_maximum' not in profile.keys():
                ph_max = 7.25
            elif profile['ph_maximum'] is "":
                ph_max = 7.25
            else:
                ph_max = profile['ph_maximum']
            if 'salinity_tolerance' not in profile.keys():
                ec_min =600
                ec_max =700
            elif profile['salinity_tolerance'] == "":
                ec_min =600
                ec_max =700
            elif profile['salinity_tolerance'] == "none":
                ec_min =200
                ec_max =300
            elif profile['salinity_tolerance'] == "low":
                ec_min =400
                ec_max =500
            elif profile['salinity_tolerance'] == "medium":
                ec_min =600
                ec_max =700
            elif profile['salinity_tolerance'] == "high":
                ec_min =800
                ec_max =900
            else:
                ec_min =600
                ec_max =700
        new_grow_controls = {"time":[], "condition" : []}
        if request.form['experiment'] == "false" and request.form['default_profile'] == "false":
            condition_control_num = 0
            time_control_num = 0

            for key in request.form.keys():
                if key[:-1] == "if_this_condition_":
                    condition_control_num+=1
                elif key[:-1] == "time_int_":
                    time_control_num+=1
                if time_control_num == 1:
                    if request.form['time_int_1'] == "":
                        time_control_num = 0
                if condition_control_num == 1:
                    if request.form['if_this_condition_1'] == "":
                        condition_control_num = 0
            
            for i in range(time_control_num):
                if str(request.form['actuator_control_'+str(i+1)+'_actuator']) in actuators.keys():
                    new_grow_controls["time"].append({"action": "toggle",
                    "actuator": request.form['actuator_control_'+str(i+1)+'_actuator'],
                    "unit": request.form['time_hour_min_'+str(i+1)],
                    "value": int(request.form['time_int_'+str(i+1)]),
                    "start_date" : request.form['startdate_activity_'+str(i+1)],
                    "finish_date" : request.form['finishdate_activity_'+str(i+1)]})
            
            for i in range(condition_control_num):
                if request.form['if_this_condition_'+str(i+1)] in sensors and \
                                request.form['do_this_condition_'+str(i+1)].split("-")[0] in actuators.keys():
                    new_grow_controls["condition"].append({"action": (request.form['do_this_condition_'+str(i+1)].split("-")[1]),
                    "actuator": request.form['do_this_condition_'+str(i+1)].split("-")[0],
                    "sensor" : request.form['if_this_condition_'+str(i+1)],
                    "operator" : request.form['is_condition_'+str(i+1)].split("%")[0],
                    "unit": request.form['if_this_condition_'+str(i+1)],
                    "value": float(request.form['to_this_condition_'+str(i+1)])})
        if request.form['experiment'] == "false" and request.form['default_profile'] == "true":
            if "light_1" in actuators.keys():
                new_grow_controls["time"].append({"action": "toggle",
                    "actuator": "light_1",
                    "unit": "hours",
                    "value": 12 })
            if "light_2" in actuators.keys():
                new_grow_controls["time"].append({"action": "toggle",
                "actuator": "light_2",
                "unit": "hours",
                "value": 12 })
            if "water_pump" in actuators.keys():
                new_grow_controls["time"].append({"action": "toggle",
                "actuator": "water_pump",
                "unit": "minutes",
                "value": 15 })
            if "pH" in sensors:
                if "phUpper_pump" in actuators.keys():
                    new_grow_controls["condition"].append({"action": "on",
                    "actuator": "phUpper_pump",
                    "operator" : "<",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": ph_min})
                    new_grow_controls["condition"].append({"action": "off",
                    "actuator": "phUpper_pump",
                    "operator" : ">",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": ph_min})
                if "phDowner_pump" in actuators.keys():
                    new_grow_controls["condition"].append({"action": "on",
                    "actuator": "phDowner_pump",
                    "operator" : ">",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": ph_max})
                    new_grow_controls["condition"].append({"action": "off",
                    "actuator": "phDowner_pump",
                    "operator" : "<",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": ph_max})
            if "EC" in sensors:       
                if "nutrient_pump" in actuators.keys():     
                    new_grow_controls["condition"].append({"action": "on",
                    "actuator": "nutrient_pump",
                    "operator" : "<",
                    "unit": "EC",
                    "sensor" : "EC",
                    "value": ec_min})
                    new_grow_controls["condition"].append({"action": "off",
                    "actuator": "nutrient_pump",
                    "operator" : ">",
                    "unit": "EC",
                    "sensor" : "EC",
                    "value": ec_max})
        if request.form['experiment'] == "true":
            if "light_1" in actuators.keys():
                value = int(request.form['lights'].split("H")[0])
                new_grow_controls["time"].append({"action": "on",
                "actuator": "light_1",
                "unit": "hours",
                "value": value })
            if "light_2" in actuators.keys():
                value = int(request.form['lights'].split("H")[0])
                new_grow_controls["time"].append({"action": "on",
                "actuator": "light_2",
                "unit": "hours",
                "value": value })
            if "water_pump" in actuators.keys():
                value = int(request.form['water'].split("min")[0])
                new_grow_controls["time"].append({"action": "toggle",
                "actuator": "water_pump",
                "unit": "minutes",
                "value": value })
            if "pH" in sensors:
                if "phUpper_pump" in actuators.keys():
                    if request.form['pH'] == "pH_below_default":
                        value_min = ph_min - .25
                    elif request.form['pH'] == "pH_above_default":
                        value_min = ph_min + .25
                    new_grow_controls["condition"].append({"action": "on",
                    "actuator": "phUpper_pump",
                    "operator" : "<",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": value_min })
                    new_grow_controls["condition"].append({"action": "off",
                    "actuator": "phUpper_pump",
                    "operator" : ">",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": value_min})
                if "phDowner_pump" in actuators.keys():
                    if request.form['pH'] == "pH_below_default":
                        value_max = ph_max - .25
                    elif request.form['pH'] == "pH_above_default":
                        value_max = ph_max + .25
                    new_grow_controls["condition"].append({"action": "on",
                    "actuator": "phDowner_pump",
                    "operator" : ">",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": value_max})
                    new_grow_controls["condition"].append({"action": "off",
                    "actuator": "phDowner_pump",
                    "operator" : "<",
                    "unit": "pH",
                    "sensor" : "pH",
                    "value": value_max})
            if "EC" in sensors:       
                if "nutrient_pump" in actuators.keys():
                    if request.form['ec'] == "ec_below_default":
                            value_min = ec_min - 100
                            value_max = ec_max - 100
                    elif request.form['ec'] == "ec_above_default":
                            value_min = ec_min + 100
                            value_max = ec_max + 100
                        
                    new_grow_controls["condition"].append({"action": "on",
                    "actuator": "nutrient_pump",
                    "operator" : "<",
                    "unit": "EC",
                    "sensor" : "EC",
                    "value": value_min})
                    new_grow_controls["condition"].append({"action": "off",
                    "actuator": "nutrient_pump",
                    "operator" : ">",
                    "unit": "EC",
                    "sensor" : "EC",
                    "value": value_max})
        
        new_grow = {"grow_name" : request.form['grow_name'], "plant_profile": request.form['plant_type'], "experiment" :request.form['experiment'], "device_name" : request.form['device_name'], "device_id":device_id, \
                        "username":username, "sensors":sensors, "actuators":actuators, "controls": new_grow_controls }
        db.grows.insert_one(new_grow)
        return redirect(url_for('grows.list_grow', current_grow=request.form['grow_name']))
    else:
        return redirect(url_for('plant_profiles.list_plant_profiles', num=num))

@mod_grows.route('/delete_grow/<grow_name>', methods=['POST'])
@login_required
def delete_grow(grow_name):
    username = current_user.get_id()

    device = db.grows.delete_one({'grow_name' : grow_name})
    return redirect(url_for('plant_profiles.list_plant_profiles'))



