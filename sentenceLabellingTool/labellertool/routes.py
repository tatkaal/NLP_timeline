import traceback
from time import strftime

from flask import request, jsonify, make_response, render_template, url_for, flash, redirect

from labellertool.config.cfg_handler import CfgHandler
from labellertool.config.cfg_utils import fetch_base_url

from labellertool.generate_data import sentencelabel
import csv
from labellertool.appendTable import loader

from flask_login import login_user, current_user, logout_user, login_required
from labellertool import app, db, bcrypt
from labellertool.forms import RegistrationForm, LoginForm
from labellertool.models import User, Post

# Initialize the Flask application
# app = Flask(__name__)

counter = 0

@app.route('/')
@app.route('/home')
def home():
    # base_url = fetch_base_url(CfgHandler())
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # next_page = request.args.get('next')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
    
@app.route('/index')
@login_required
def index():
    base_url = fetch_base_url(CfgHandler())
    return render_template('index.html', base_url=base_url)

@app.route('/v1/label', methods=['GET'])
@login_required
def label():
    global counter
    app.logger.debug('label(): requested')
    if 'url' not in request.args:
        return make_response(jsonify({'error': str('Bad Request: argument `url` is not available')}), 400)

    url = request.args['url']

    if not url:  # if url is empty
        return make_response(jsonify({'error': str('Bad Request: `url` is empty')}), 400)

    try:
        obj = sentencelabel(url)
        sentences, pos = obj.labelit()

    except Exception as ex:
        app.logger.error('label(): error while preparing labels: ' + str(ex) + '\n' + traceback.format_exc())
        pass
    
    try:
        with open('counter.txt', 'r') as fileread:
            counter = int(fileread.read())
    except:
        pass
    print(counter, type(counter))

    with open('counter.txt', 'w') as filewrite:
        counter+=1
        filewrite.write(str(counter))

    return make_response(jsonify({'sentences': sentences,'pos':pos, 'file_index':str(counter)}))

@app.route('/save_csv', methods=['POST'])
@login_required
def save2csv():
    global counter

    category = request.form.get('category')
    pos = request.form.get('pos')
    sentences = request.form.get('sentences')
    index = request.form.get('index')

    loader(int(index), 3, category, counter)
    loader(int(index), 1, sentences, counter)

    return make_response(jsonify(''))

if __name__ == '__main__':

    app.run(
        host="localhost"
    )
