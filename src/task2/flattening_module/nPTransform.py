import numpy as np
import cv2


# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/


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
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
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
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped


def four_points_correct_aspect(image, rect, width, height):
    """
    :param image: The image to be transformed.
    :param rect: A list of 4 points in order from the top left in clockwise
    ordering.
    :param width: The length of the smallest side of the rectangle
    :param height: The length of the largest side of the rectangle
    :return: The flattened points

    *** Note this will not work well with close to square panels or images
    were the panel is far from flat on. This is because this function makes the
    assumption that the side "largest" and "smallest" sides are the same ones as
    the "largest" and "smallest" sides after projection.
    if this problem is encounterd simply swap width and height.
    """
    flattened = four_point_transform(image, rect)

    x, y = flattened.shape[:2]
    if x <= y:
        ft_width = x
        ft_height = y
        if ft_height * (width / height) > ft_width:
            new_image_size = (ft_height, int(ft_height*(width/height)))
        else:
            new_image_size = (int(ft_width*(height/width)), ft_width)
    else:
        ft_width = x
        ft_height = y
        if ft_height * (width / height) > ft_width:
            new_image_size = (int(ft_height*(width/height)), ft_height)
        else:
            new_image_size = (ft_width, int(ft_width*(height/width)))

    return cv2.resize(flattened, new_image_size, interpolation=cv2.INTER_CUBIC)


if __name__ == '__main__':
    pass
    # fourpoints = np.array([[13., 127.], [492., 14.], [631., 293.], [118., 455.]], np.float32)
    # image = cv2.imread("Sample_Images/book.png")
    # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    # plt.show()
    # a = four_point_transform(image, fourpoints)
    # cv2.imwrite("result.png", a)

