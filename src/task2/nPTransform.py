import numpy as np
import cv2
import Rectangle
import gui
from matplotlib import pyplot as plt


# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
# TODO change maxwidth and height to the actual size of the solar panel

def input_solar_panel_rect(solar_panel_rect):
    w = input("Input the Solar Panel Width")
    h = input("Input the Solar Panel Height")

def four_point_transform(image, rect):
    # obtain a consistent order of the points and unpack them
    # individually
    tl, tr, br, bl = rect[0], rect[1], rect[2], rect[3]

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    print widthA, widthB, maxWidth
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    print heightA, heightB, maxHeight
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    print dst
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped

def tuple2array():
    return NotImplemented


if __name__ == '__main__':
    # gui.gui()
    fourpoints = np.array([[13., 127.], [492., 14.], [631., 293.], [118., 455.]], np.float32)
    image = cv2.imread("Sample_Images/book.png")
    plt.imshow(image)
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
    a = four_point_transform(image, fourpoints)
    cv2.imwrite("result.png", a)

