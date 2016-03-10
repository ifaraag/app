# Import flask and template operators
from flask import Flask, render_template, redirect
#from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers

client = MongoClient("mongodb://admin:admin@ds011268.mlab.com:11268/analytics-hydrobase")
db = client['analytics-hydrobase']

#Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return redirect('https://github.com/404'), 404

# Import a module / component using its blueprint handler variable 
from app.views import mod_app
from app.auth.views import mod_auth
from app.dashboard.views import mod_dashboard

# Register blueprint(s)
app.register_blueprint(mod_app)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_dashboard)

# from app import views
# from app.auth import views
# from app.dashboard import views
