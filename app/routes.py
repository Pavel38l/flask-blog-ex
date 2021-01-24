import os
from app import app
from app.forms import LoginForm, UploadForm
from flask import render_template, flash, redirect, url_for, request
from app import generator
from werkzeug.utils import secure_filename
import time

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Эльдар Рязанов'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        print("try save image")
        filename = f"{generator.next()}.{get_extension(file.filename)}"#secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed')
        transform(filename)
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)


def transform(filename):
    if os.path.isfile(os.path.join(app.config['UPLOADED_IMAGES_DEST'], f"out_{filename}")):
        print("dfd")


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']