from flask import render_template, redirect, url_for, request
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome to Hydrobase')

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
    return render_template('login.html',
                           title='Login to Hydrobase',
                           form=form,
                           error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Your Dashboard')
