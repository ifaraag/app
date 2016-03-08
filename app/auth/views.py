from flask import render_template, redirect, url_for, request
from app import app
from .forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin' or
            request.form['password'] != 'admin'):
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('dashboard'))
    return render_template('auth/login.html',
                           title='Login to Hydrobase',
                           form=form,
                           error=error)
