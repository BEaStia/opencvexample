from __future__ import print_function
import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt


class ImageFinder(object):
    FIRST_IMAGE = 1
    SECOND_IMAGE = 2
    THIRD_IMAGE = 3

    def __init__(self):
        self.first = None
        self.second = None
        self.third = None
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        pass

    def read_and_transform_image(self, path, pos):
        img = cv2.imread(path, 0)
        kernel = np.ones((5, 5), np.float32) / 25
        dst = cv2.filter2D(img, -1, kernel)
        cv2.Canny(dst, 100, 200)
        ret, thresh = cv2.threshold(dst, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(dst, contours, -1, (0, 255, 0), -1)
        if pos == self.FIRST_IMAGE:
            self.first = dst
        elif pos == self.SECOND_IMAGE:
            self.second = dst
        elif pos == self.THIRD_IMAGE:
            self.third = dst

    def display_plots(self):
        self.ax1 = plt.subplot2grid((3, 3), (0, 0))
        self.ax1.set_title("first")
        plt.sca(self.ax1)
        plt.imshow(self.first, cmap='gray')
        plt.axis('off')

        self.ax2 = plt.subplot2grid((3, 3), (0, 1))
        self.ax2.set_title("second")
        plt.sca(self.ax2)
        plt.imshow(self.second, cmap='gray')
        plt.axis('off')

        self.ax3 = plt.subplot2grid((3, 3), (1, 0))
        self.ax3.set_title("third")
        plt.sca(self.ax3)
        plt.imshow(self.third, cmap='gray')

        plt.axis('off')
        plt.subplots_adjust(left=0.18)
        binding_id = plt.connect('motion_notify_event', self.on_move)
        plt.connect('button_press_event', self.on_click)
        plt.show()

    def on_move(self, event):
        # get the x and y pixel coords
        x, y = event.x, event.y

        if event.inaxes:
            ax = event.inaxes  # the axes instance
            print('data coords %f %f' % (event.xdata, event.ydata))

    def on_click(self, event):
        # get the x and y coords, flip y from top to bottom
        print('enter_figure', event.canvas.figure)
        x, y = event.x, event.y
        if event.button == 1:
            if event.inaxes is not None:
                if event.inaxes == self.ax1:
                    print('data coords %f %f at first' % (event.xdata, event.ydata))
                elif event.inaxes == self.ax2:
                    print('data coords %f %f at second' % (event.xdata, event.ydata))
                elif event.inaxes == self.ax3:
                    print('data coords %f %f at third' % (event.xdata, event.ydata))



finder = ImageFinder()
finder.read_and_transform_image("image.jpg", 1)
finder.read_and_transform_image("image.jpg", 2)
finder.read_and_transform_image("image.jpg", 3)
finder.display_plots()
