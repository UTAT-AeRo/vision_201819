import numpy as np

class Rectangle:
    """
    (x. y)
    """
    def __init__(self):
        self.top_left = np.array([0, 0])
        self.bottom_right = np.array([1, 1])

    # Set
    def set_top_left(self, top_left):
        self.top_left = top_left

    def set_bottom_right(self, bottom_right):
        self.bottom_right = bottom_right

    # Get
    def get_width_pixels(self):
        """
        :return: width in pixels
        """
        return  abs(self.top_left[0] - self.bottom_right[0])

    def get_height_pixels(self):
        return abs(self.top_left[1] - self.bottom_right[1])

    def get_rectange_coords(self):
        """
        Gives a 4x2 matrix with the four corner coordinates clockwise from top-left
        :return:  top-left, top-right, bottom-right, bottom-left in a 4x2 matrix
        """
        rect_shape = (4, 2)
        rect = np.empty(rect_shape)
        rect[0] = self.top_left
        rect[1] = np.array([self.bottom_right[0], self.top_left[1]])
        rect[2] = self.bottom_right
        rect[3] = np.array([self.top_left[0], self.bottom_right[1]])
        return rect
