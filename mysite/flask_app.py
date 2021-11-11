from flask import Flask
from flask.templating import render_template
import tensorflow as tf
import classify as cl

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/index2")
def index2():
    return str(tf.reduce_sum(tf.random.normal([1000, 1000])))

@app.route("/classify")
def classify():
    return cl.most_color('images/red.png')
