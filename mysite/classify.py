import numpy as np
import cv2 as cv

# test_image = "r100g200b255.png"
# img = cv.imread(test_image)
# cv.imshow("image", img)
# cv.waitKey()

def most_color(img_file):
    img = cv.imread(img_file)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    height, width, channels = img.shape
    # print(height, width)

    red = 0
    green = 0
    blue = 0
    for x in range(0,width-1):
        for y in range(0,height-1):
            red += img[y][x][0]
            green += img[y][x][1]
            blue += img[y][x][2]
    # print(red/(height*width))
    # print(green/(height*width))
    # print(blue/(height*width))

    # cv.imshow("image", img)
    # cv.waitKey(0)

    if red > green and red > blue:
        return "red"
    elif green > red and green > blue:
        return "green"
    else:
        return "blue"

if __name__=="__main__":
    test_image = "red.png"
    print(most_color(test_image))