from flask import Flask, render_template, request, url_for
import tensorflow as tf
import classify as cl
import os

USER_UPLOADS = '~/arachnid/images'

app = Flask(__name__)
app.config['USER_UPLOADS'] = USER_UPLOADS

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index2")
def index2():
    return str(tf.reduce_sum(tf.random.normal([1000, 1000])))

@app.route("/classify")
def classify():
    return cl.most_color('images/red.png')

@app.route("/img_upload", methods=['POST'])
def upload_img():
    uploaded_image = request.files['file']
    if uploaded_image.filename != '':
        open(os.path.join(app.config[USER_UPLOADS], uploaded_image.filename)).write(uploaded_image)
        return 1
    return 0

@app.route("/test_upload", methods=['GET','POST'])
def test_upload():
    return render_template('upload.html')