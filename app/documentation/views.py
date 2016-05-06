from flask import Blueprint, render_template, Response
from flask.ext.login import login_required, current_user

# Define the blueprint: 'documentation'
mod_documentation = Blueprint('documentation', __name__)

@mod_documentation.route('/documentation')
@login_required
def documentation():
	pass