from flask import Flask, render_template, redirect
from pymongo import MongoClient
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)

client = MongoClient("mongodb://admin:admin@ds011268.mlab.com:11268/analytics-hydrobase")
db = client['analytics-hydrobase']

from app.views import mod_app
from app.auth.views import mod_auth
from app.dashboard.views import mod_dashboard

app.register_blueprint(mod_app)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_dashboard)

@app.errorhandler(404)
def not_found(error):
    return redirect('https://github.com/404'), 404
