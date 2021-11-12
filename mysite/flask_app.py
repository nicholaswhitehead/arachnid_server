from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import classify as cl
import os
import time

USER_UPLOADS = '/home/nicowhitehead/arachnid/images'

app = Flask(__name__)
app.config['USER_UPLOADS'] = USER_UPLOADS

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/tensorflow_test")
def index2():
    return str(tf.reduce_sum(tf.random.normal([1000, 1000])))

@app.route("/dummy_test")
def classify():
    return cl.most_color('images/red.png')

@app.route("/img_upload", methods=['GET','POST'])
def upload_img():
    if request.method=='POST':
        uploaded_image = request.files['file']
        if uploaded_image.filename != '':
            start = time.time()
            image_filepath = os.path.join(app.config['USER_UPLOADS'], uploaded_image.filename)
            uploaded_image.save(image_filepath)
            middle = time.time()
            color = cl.most_color(image_filepath)
            end = time.time()

            filewritetime = middle - start
            classifytime = end - middle

            return str([filewritetime, classifytime, color])
            # return redirect(url_for('test_upload'))
    return render_template('upload.html')