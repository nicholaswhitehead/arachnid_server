from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import classify as cl
import os

USER_UPLOADS = '/home/nicowhitehead/arachnid/images'

app = Flask(__name__)
app.config['USER_UPLOADS'] = USER_UPLOADS

# Main website homescreen
@app.route("/")
def index():
    return render_template('index.html')

# Tests a TensorFlow call - ensures packages installed correctly on PythonAnywhere
@app.route("/tensorflow_test")
def index2():
    return str(tf.reduce_sum(tf.random.normal([1000, 1000])))

# Tests the classify model
@app.route("/dummy_test")
def classify():
    return cl.most_color('images/red.png')

# Tests file upload to the server, accessible through browser
@app.route("/img_upload", methods=['GET','POST'])
def upload_img():
    if request.method=='POST':
        uploaded_image = request.files['file']

        # ensure file exists and is of correct type
        if uploaded_image.filename == '':
            return "No file received: PNG expected."
        if uploaded_image.filename[-4:] != ".png":
            return "Unacceptable filetype: PNG expected."
        
        # write input image to drive
        image_filepath = os.path.join(app.config['USER_UPLOADS'], uploaded_image.filename)
        uploaded_image.save(image_filepath)

        color = cl.most_color(image_filepath)

        # remove image
        os.remove(image_filepath)

        return color
        # return redirect(url_for('img_upload'))

    return render_template('upload.html')