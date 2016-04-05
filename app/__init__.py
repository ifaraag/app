from flask import Flask, render_template, redirect
from pymongo import MongoClient
from flask_login import LoginManager
from pubnub import Pubnub

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

def _callback(message, channel):
    print(message)

def sub_callback(message, channel):
	db.data.insert_one(message)

# Grant read, write and manage permissions to the pubnub instance that we initialized
pubnub.grant(channel_group='hydrobase', auth_key=app.config['PUBNUB_AUTH_KEY'], read=True, write=True, manage=True, ttl=0, callback=_callback, error=_callback)

# Subscribe to the channel group 'hydrobase' that contains the channels for all users to get the data 
# coming in from different devices and put that into the DB
pubnub.subscribe_group(channel_groups=app.config['PUBNUB_CHANNEL_GRP'], callback=sub_callback, error=_callback)


from app.views import mod_app
from app.auth.views import mod_auth
from app.dashboard.views import mod_dashboard
from app.devices.views import mod_devices
from app.grows.views import mod_grows
from app.experiments.views import mod_experiments

app.register_blueprint(mod_app)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_dashboard)
app.register_blueprint(mod_devices)
app.register_blueprint(mod_grows)
app.register_blueprint(mod_experiments)

@app.errorhandler(404)
def not_found(error):
    return redirect('https://github.com/404'), 404
