from __future__ import print_function

import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

#create db connector
os.remove('my_database.db')
db = SqliteExtDatabase('my_database.db')

#base model class to extend it
class BaseModel(Model):
    class Meta:
        database = db


#point at all rows at once
class MultiDimensionalPoint(BaseModel):
    first_pos_x = FloatField()
    first_pos_y = FloatField()
    second_pos_x = FloatField()
    second_pos_y = FloatField()
    third_pos_x = FloatField()
    third_pos_y = FloatField()

    def __init__(self):
        self.first_pos_x = self.first_pos_y = 0
        self.second_pos_y = self.second_pos_x = 0
        self.third_pos_x = self.third_pos_y = 0

#helper
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
        self.first_path = 'image.jpg'
        self.second_path = 'image.jpg'
        self.third_path = 'image.jpg'
        self.points = []
        self.current_point = None
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
        x, y = event.x, event.y
        if event.button == 1:
            if event.inaxes is not None:
                if self.current_point is None:
                    self.current_point = MultiDimensionalPoint()
                if event.inaxes == self.ax1:
                    self.current_point.first_pos_x = x
                    self.current_point.first_pos_y = y
                elif event.inaxes == self.ax2:
                    self.current_point.second_pos_x = x
                    self.current_point.second_pos_y = y
                elif event.inaxes == self.ax3:
                    self.current_point.third_pos_x = x
                    self.current_point.third_pos_y = y

    def save(self):
        if self.current_point is not None:
            self.current_point.save()
            self.points.append(self.current_point)
        self.current_point = MultiDimensionalPoint()

#connect to db
db.connect()
#create tables
db.create_tables([MultiDimensionalPoint])

finder = ImageFinder()

#add buttons
resetax = plt.axes([0.7, 0.025, 0.1, 0.04])
button = Button(resetax, 'Load files', color='lightgoldenrodyellow', hovercolor='0.975')

resetax_save = plt.axes([0.85, 0.025, 0.1, 0.04])
button_save = Button(resetax_save, 'Save point', color='lightgoldenrodyellow', hovercolor='0.975')


def load(event):
    finder.read_and_transform_image(finder.first_path, 1)
    finder.read_and_transform_image(finder.second_path, 2)
    finder.read_and_transform_image(finder.third_path, 3)
    finder.display_plots()


def save(event):
    finder.save()


button_save.on_clicked(save)
button.on_clicked(load)
plt.show()
