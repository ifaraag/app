from flask import Flask, render_template, redirect
from pymongo import MongoClient
from flask_login import LoginManager
from pubnub import Pubnub
import datetime

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)

#initialize the mongodb instance
client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['DB_NAME']]

#initialize the pubnub instance
pubnub = Pubnub(publish_key=app.config['PUBNUB_PUBLISH_KEY'], \
	subscribe_key=app.config['PUBNUB_SUBSCRIBE_KEY'], secret_key=app.config['PUBNUB_SECRET_KEY'], \
		auth_key=app.config['PUBNUB_AUTH_KEY'])

def _callback(message):
    print(message)

def _error(message):
	print(message)

def sub_callback(message, channel):
	# print(channel)
	if "CV_Data" in message.keys():
		pass
		# print message
		# db.cv_data.insert_one(message)
	elif 'sender' in message.keys():
		message_array  = []
		utc_datetime = datetime.datetime.utcnow()
		message['year'] = utc_datetime.year
		message['month'] = utc_datetime.month
		message['day'] = utc_datetime.day
		message['hour'] = utc_datetime.hour
		message['min'] = utc_datetime.minute
		message['sec'] = utc_datetime.second
		if 'EC' in message.keys():
			message['TDS'] = message['EC'].split(",")[1]
			message['PS'] = message['EC'].split(",")[2]
			message['EC'] = message['EC'].split(",")[0]

		device_id = message['sender']['device_id']
		message['device_id'] = device_id
		message.pop('sender', None)
		related_grows = db.grows.find({'device_id' : device_id})
		for grow in related_grows:
			message_temp = message.copy()
			message_temp['grow_name'] = grow['grow_name']
			message_array.append(message_temp)
		
		# print message_array
		# db.data.insert_many(message_array)
		# db.backup.insert_one(message)

# Grant read, write and manage permissions to the pubnub instance that we initialized
pubnub.grant(channel_group='hydrosmart', auth_key=app.config['PUBNUB_AUTH_KEY'], read=True, write=True, manage=True, ttl=0, callback=_callback, error=_error)

# Subscribe to the channel group 'hydrosmart' that contains the channels for all users to get the data 
# coming in from different devices and put that into the DB
pubnub.subscribe_group(channel_groups=app.config['PUBNUB_CHANNEL_GRP'], callback=sub_callback, error=_error)

from app.views import mod_app
from app.auth.views import mod_auth
from app.dashboard.views import mod_dashboard
from app.devices.views import mod_devices
from app.grows.views import mod_grows
from app.plant_profiles.views import mod_plant_profiles
from app.documentation.views import mod_documentation

app.register_blueprint(mod_app)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_dashboard)
app.register_blueprint(mod_devices)
app.register_blueprint(mod_grows)
app.register_blueprint(mod_plant_profiles)
app.register_blueprint(mod_documentation)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html')
    #return redirect('404.html'), 404

def notifications(username):
	notifications  = db.notifications.find({"username" : username}).limit(10)


