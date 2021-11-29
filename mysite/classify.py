import numpy as np
import cv2 as cv

def most_color(img_file):
    img = cv.imread(img_file)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    height, width, channels = img.shape

    red = np.sum(img[:,:,0])
    green = np.sum(img[:,:,1])
    blue = np.sum(img[:,:,2])

    if red == green and green == blue:
        return "gray"

    if red > green and red > blue:
        return "red"
    elif green > red and green > blue:
        return "green"
    else:
        return "blue"

if __name__=="__main__":
    test_image = "C:/Users/Nicholas/Documents/GitHub/arachnid/images/green.png"
    print(most_color(test_image))