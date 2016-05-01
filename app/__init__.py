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
	utc_datetime = datetime.datetime.utcnow()
	message['year'] = utc_datetime.year
	message['month'] = utc_datetime.month
	message['day'] = utc_datetime.day
	message['hour'] = utc_datetime.hour
	message['min'] = utc_datetime.minute
	message['sec'] = utc_datetime.second
	message['TDS'] = message['EC'].split(",")[1]
	message['PS'] = message['EC'].split(",")[2]
	message['EC'] = message['EC'].split(",")[0]

	result = db.grows.update_one(
      { "grow_name" : 'Avi'},
      {
      '$push': {'data':message}
      },
      upsert=True
      )

	db.data.insert_one(message)

# Grant read, write and manage permissions to the pubnub instance that we initialized
pubnub.grant(channel_group='hydrobase', auth_key=app.config['PUBNUB_AUTH_KEY'], read=True, write=True, manage=True, ttl=0, callback=_callback, error=_error)

# Subscribe to the channel group 'hydrobase' that contains the channels for all users to get the data 
# coming in from different devices and put that into the DB
pubnub.subscribe_group(channel_groups=app.config['PUBNUB_CHANNEL_GRP'], callback=sub_callback, error=_error)

from app.views import mod_app
from app.auth.views import mod_auth
from app.dashboard.views import mod_dashboard
from app.devices.views import mod_devices
from app.grows.views import mod_grows
from app.plant_profiles.views import mod_plant_profiles

app.register_blueprint(mod_app)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_dashboard)
app.register_blueprint(mod_devices)
app.register_blueprint(mod_grows)
app.register_blueprint(mod_plant_profiles)

@app.errorhandler(404)
def not_found(error):
    return redirect('https://github.com/404'), 404


