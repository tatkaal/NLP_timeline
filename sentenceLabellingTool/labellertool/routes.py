import traceback
from time import strftime

from flask import request, jsonify, make_response, render_template, url_for, flash, redirect

from labellertool.generate_data import sentencelabel
import csv
from labellertool.appendTable import loader

from flask_login import login_user, current_user, logout_user, login_required
from labellertool import app, db, bcrypt
from labellertool.forms import RegistrationForm, LoginForm
from labellertool.models import User, Post
from werkzeug.utils import secure_filename
import os
from labellertool.config import resumePath, labelledDataPath
import pandas as pd

# Initialize the Flask application
# app = Flask(__name__)

counter = 0

@app.route('/', methods=['GET'])
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
    # base_url = fetch_base_url(CfgHandler())
    return render_template('index.html')

@app.route('/', methods=['POST'])
@login_required
def label():
    global counter
    # print(request.method)
    # app.config['UPLOAD_FOLDER'] = 'labellertool/resume/'
    # resumePath = 'labellertool/resume/'
    # print(request.files)
    if request.method == 'POST':
        # f = request.files.getlist("file")
        # print(request.files.getlist('file'))
        # print('**********************************')
        f = request.files.getlist("file")
        for each_file in f:
            # print('----------------------------------------',secure_filename(each_file.filename))
            # print(os.path.join(resumePath,secure_filename(each_file.filename)))
            each_file.save(os.path.join(resumePath,secure_filename(each_file.filename)))
        print('files uploaded successfully')
        # for resumefile in f:
        #     filename = resumefile.filename
        #     print('##############################', filename)

        try:
            obj = sentencelabel(resumePath)
            sentences = obj.labelit()
            for each_file in f:
                # print('--------------------------')
                # print(os.path.join(resumePath,secure_filename(each_file.filename)))
                os.remove(os.path.join(resumePath,secure_filename(each_file.filename)))

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
        # print({'sentences': sentences,'pos':pos})

        # cnt = [val for i in len(sentences)]
        cnt = list(range(1,len(sentences)+1))
        data = pd.DataFrame({'S.No.':cnt,'Sentences':sentences})
        data['Category'] = ''
        data.to_csv(f'{labelledDataPath}/test-{counter}.csv', index=False)
        return make_response(jsonify({'sentences': sentences, 'file_index':str(counter)}))

        # return make_response(jsonify({'sentences':['euta cha', 'duita cha'],'pos':['a','b'],'file_index':str(counter)}))
    else:
        return 'not working......................'

@app.route('/save_csv', methods=['POST'])
@login_required
def save2csv():
    global counter

    category = request.form.get('category')
    # pos = request.form.get('pos')
    sentences = request.form.get('sentences')
    index = request.form.get('index')

    loader(int(index), 3, category, counter)
    loader(int(index), 1, sentences, counter)

    return make_response(jsonify(''))

@app.route('/counter', methods=['GET'])
@login_required
def return_counter():
    return counter
# @app.route('/downloadData/')
# def downloadData():
# #   print ('I got clicked!')

#   return send_from_directory(directory=os.getcwd()+"/files", filename="filename.txt")
