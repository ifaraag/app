from flask import Blueprint, render_template


# Define the blueprint: 'dashboard'
mod_dashboard = Blueprint('dashboard', __name__)

@mod_dashboard.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html',
                           title='Your Dashboard')
