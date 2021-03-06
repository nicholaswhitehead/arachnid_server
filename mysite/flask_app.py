from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import tensorflow as tf
import classify as cl
import os
import io
import time
from PIL import Image

USER_UPLOADS = '/home/nicowhitehead/arachnid/images'

app = Flask(__name__)
app.config['USER_UPLOADS'] = USER_UPLOADS
app.config['MAX_CONTENT_LENGTH'] = 8192 * 8192

# SQL set up code modified from pythonanywhere tutorial at https://blog.pythonanywhere.com/121/
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="nicowhitehead",
    password="spiderdbpass",
    hostname="nicowhitehead.mysql.pythonanywhere-services.com",
    databasename="nicowhitehead$spiderresults",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Spider(db.Model):
    __tablename__ = "spiders"
    spider_id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(50))
    venom = db.Column(db.Integer)
    text = db.Column(db.String(200))


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
    classification = cl.classify(r'/home/nicowhitehead/arachnid/images/tigrosa.jpg')
    spider = Spider.query.filter_by(spider_id=int(classification)).first()
    output = '|'.join([spider.species, str(spider.venom), spider.text])
    return output

# Upload an image file to the server
@app.route("/img_upload", methods=['POST'])
def upload_img():
    if request.method == 'POST':
        # ensure file is not empty
        if len(request.get_data()) == 0:
            return "No file received: JPEG expected."

        # every call writes to a unique file to eliminate read/write conflicts between multiple users
        current_time = time.process_time()
        image_filepath = os.path.join(app.config['USER_UPLOADS'], f"{current_time}.jpeg")
        image = Image.open(io.BytesIO(request.get_data()))

        image_orientation = image.getexif()[0x0112] # 'Orientation' Exif tag
        # print(image_orientation, file=sys.stderr)

        # https://sirv.sirv.com/website/exif-orientation-values.jpg?scale.option=fill&scale.width=512&scale.height=252
        # mirrored images are not a feasible response from the Android app; only 3,6,8 need to be considered.
        if image_orientation == 3:
            image = image.rotate(180, expand=1)
        elif image_orientation == 6:
            image = image.rotate(270, expand=1) # rotation is counter-clockwise
        elif image_orientation == 8:
            image = image.rotate(90, expand=1)

        image.save(image_filepath)
        classification = cl.classify(image_filepath) # classify uses VGG16-based model to predict class of image
        spider = Spider.query.filter_by(spider_id=int(classification)).first()
        output = '|'.join([spider.species, str(spider.venom), spider.text])
        os.remove(image_filepath)
        return output
    else:
        # Currently broken - file upload expected in Byte array, not multipart form file
        return render_template('upload.html')