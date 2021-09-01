#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   30 Aug 2021
#

from flask import request, session, redirect
from flask.templating import render_template
from config.config import app
from model.user import User

@app.before_request
def verify_logged():
    app.logger.debug('Reuqest path: %s' % request.path)
    if 'logged_user_id' not in session and request.path not in ['/', '/static/bootstrap.min.css', '/signup', '/login']:
        return redirect('/login')

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    email = None
    if 'email' in request.form:
        email = request.form['email']
    if email is None or len(email.strip()) == 0:
        return render_template('signup_error.html', message='Invalid email !!!')
    password1 = None
    if 'password1' in request.form:
        password1 = request.form['password1']
    if password1 is None or len(password1.strip()) == 0:
        return render_template('signup_error.html', message='Invalid password !!!')
    password2 = None
    if 'password2' in request.form:
        password2 = request.form['password2']
    if password1 != password2:
        return render_template('signup_error.html', message='Password confirmation failed !!!')
    user = User.register(email, password1)
    app.logger.info('User %s successfully registered!' % user)
    return render_template('welcome.html')

@app.route('/login', methods=['POST'])
def login():
    email = None
    if 'email' in request.form:
        email = request.form['email']
    if email is None or len(email.strip()) == 0:
        return render_template('login_error.html', message='Invalid email !!!')
    password1 = None
    if 'password' in request.form:
        password = request.form['password']
    if password is None or len(password.strip()) == 0:
        return render_template('login_error.html', message='Invalid password !!!')
    user = User.query_by_email(email)
    if user is None:
        return render_template('login_error.html', message='Invalid email !!!')
    if not user.verify_password(password):
        return render_template('login_error.html', message='Invalid password !!!')
    session['logged_user_id'] = email
    return redirect('/secure', code=307)

@app.route('/secure', methods=['POST'])
def secure():
    return render_template('secure_notes.html')

@app.route('/logout', methods=['GET'])
def logoff():
    session.pop('logged_user_id', None)
    return render_template('welcome.html')
