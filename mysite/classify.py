import numpy as np
import cv2 as cv
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import VGG16
import timeit

# Placeholder method exclusively used for testing, in place of classify() call inside flask_app.py
# Returns the max sum of R, B, G values across all pixels in image
def most_color(img_file):
    img = cv.imread(img_file)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    height, width, channels = img.shape

    red = np.sum(img[:,:,0])
    green = np.sum(img[:,:,1])
    blue = np.sum(img[:,:,2])

    if red == green and green == blue:
        return "gray,0,extra info"

    if red > green and red > blue:
        return "red,1,extra info"
    elif green > red and green > blue:
        return "green,0,extra info"
    else:
        return "blue,1,extra info"

#
def classify(img_file, verbose=True):
    start = [] # used for timing each function call in classify()
    stop = []

    start.append(timeit.default_timer())
    img = cv.resize(cv.imread(img_file, cv.IMREAD_COLOR), (160, 160), interpolation=cv.INTER_CUBIC)
    img_arr = tf.keras.utils.img_to_array(img)
    img_arr = np.expand_dims(img_arr, axis=0)
    stop.append(timeit.default_timer())

    start.append(timeit.default_timer())
    modelVGG16 = VGG16(include_top=False, weights='imagenet')
    stop.append(timeit.default_timer())

    start.append(timeit.default_timer())
    modelFC = keras.models.load_model(r'/home/nicowhitehead/arachnid/mysite/vgg16_bottle')
    stop.append(timeit.default_timer())

    start.append(timeit.default_timer())
    features = modelVGG16.predict(img_arr)
    stop.append(timeit.default_timer())

    start.append(timeit.default_timer())
    prediction = np.argmax(modelFC.predict(features))
    stop.append(timeit.default_timer())

    # Total response time generally within 1.5-3s
    if (verbose):
        print("File reading, reshaping:")
        print('Time: ', stop[0] - start[0])
        print("Loading VGG16 model:")
        print('Time: ', stop[1] - start[1])
        print("Loading fully-connected model:")
        print('Time: ', stop[2] - start[2])
        print("Feature prediction on VGG16 model:")
        print('Time: ', stop[3] - start[3])
        print("Final prediction on FC block:")
        print('Time: ', stop[4] - start[4])

    if prediction == 0:
        return "Araneus|0|The Orb Weaver is a web-making species that typically dwells outdoors. Their largest webs are often seen in the Fall season."
    elif prediction == 1:
        return "Latrodectus|2|Black Widows often make their webs near man-made constructions, typically in dark corners or underneath stones."
    elif prediction == 2:
        return "Pisaurina|1|The American Nursery Web Spider favors outdoor conditions. Despite their name, these spiders rarely spin a web."
    elif prediction == 3:
        return "Tigrosa|1|The Wolfspider is one of the most common species in the US, finding habitats in a wide range of conditions. These spiders favor burrows over building webs."
    else:
        return "???,?,not recognized"


if __name__=="__main__":
    test_image = "C:/Users/Nicholas/Documents/GitHub/arachnid/images/green.png"
    print(classify(test_image))