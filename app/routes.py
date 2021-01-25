import os
from app import app
from app.forms import LoginForm, UploadForm
from flask import render_template, flash, redirect, url_for, request, jsonify
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
        filename = secure_filename(file.filename)
        filename = f"{generator.next()}.{get_extension(filename)}"#secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)


@app.route('/output/<filename>')
def output_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='outputs/' + filename), code=301)


@app.route('/process', methods=['POST'])
def process():
    json = jsonify({'filename': transform(request.form['filename'])})
    clear(request.form['filename'])
    return json


def clear(filename):
    print("remove files")
    path = os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)
    outpath = os.path.join(app.config['OUTPUT_IMAGES_DEST'], get_output_filename(filename))
    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(outpath):
        os.remove(outpath)


def transform(filename):
    time.sleep(1)
    print("transform " + filename)
    # if os.path.isfile(os.path.join(app.config['UPLOADED_IMAGES_DEST'], f"out_{filename}")):
    #     print("dfd")
    output_filename = get_output_filename(filename)
    return output_filename


def get_output_filename(filename):
    image_name = filename.rsplit('.', 1)[0]
    return f'output_{image_name}.png'


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""


def allowed_file(filename):
    return get_extension(filename) in app.config['ALLOWED_EXTENSIONS']