from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import classify as cl
import os
import sys
from PIL import Image
import base64

USER_UPLOADS = '/home/nicowhitehead/arachnid/images'

app = Flask(__name__)
app.config['USER_UPLOADS'] = USER_UPLOADS
app.config['MAX_CONTENT_LENGTH'] = 8192 * 8192

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
        print("Content type: " + request.content_type, file=sys.stderr)
        print("Byte stream: " + str(request.get_data()), file=sys.stderr)

        img_data = base64.b64decode(request.get_data())
        print(img_data, file=sys.stderr)

        # ensure file is not empty
        if uploaded_image.filename == '':
            return "No file received: JPEG expected."

        # ensure file is a JPEG
        if uploaded_image.filename[-5:] != ".jpeg":
            return "Unacceptable filetype: JPEG expected."

        print("after filetype checks", file=sys.stderr)

        image_filepath = os.path.join(app.config['USER_UPLOADS'], uploaded_image.filename.split("/")[-1])
        uploaded_image.save(image_filepath)

        color = cl.most_color(image_filepath)

        return color
        # return redirect(url_for('img_upload'))
    else:
        return render_template('upload.html')