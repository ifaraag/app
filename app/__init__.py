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
pubnub = Pubnub(publish_key=app.config['PUBNUB_PUBLISH_KEY'], subscribe_key=app.config['PUBNUB_SUBSCRIBE_KEY'])

from app.views import mod_app
from app.auth.views import mod_auth
from app.dashboard.views import mod_dashboard
from app.devices.views import mod_devices

app.register_blueprint(mod_app)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_dashboard)
app.register_blueprint(mod_devices)

@app.errorhandler(404)
def not_found(error):
    return redirect('https://github.com/404'), 404
