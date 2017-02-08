import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
from color import *
from sobel import *
from mask_lanes import *
from project_lanes import *
from overlay_text import *
from transform import *

plt.rcParams['image.cmap'] = 'gray'


class Pipes:
    def __init__(self):

        with open(r'camera_cal/wide_dist_pickle.p', 'rb') as pickle_file:
            p = pickle.load(pickle_file)

        self.mtx = p['mtx']
        self.dist = p['dist']

        self.pts = np.array(((0, 690), (560, 450), (720, 450), (1280, 690)))

        self.mask_bot_left = []
        self.mask_top_left = []
        self.mask_top_right = []
        self.mask_bot_right = []

        self.left_lane = []
        self.right_lane = []

        self.left_lane_direction = None
        self.right_lane_direction = None

        self.left_lane_curvature = []
        self.right_lane_curvature = []
        self.lane_direction = []
        self.position = None

        self.polygon_points_old_left = None
        self.polygon_points_old_right = None

        self.res_left = []
        self.res_right = []

        self.margin = 100
        self.lag = 5

    def insert_new_chuck_one_out(self, array, value, max_array_length):
        array.append(value)

        if len(array) > max_array_length:
            array = array[(len(array) - max_array_length):]
        return array

    def show_mask(self, img):
        cv2.polylines(img, np.int32([self.pts]), True, (0, 0, 255), 3)
        return img

    def full_pipe(self, img):
        dst = cv2.undistort(img, self.mtx, self.dist)
        unwarped = unwarp(dst, src=self.pts)
        # find lines on undistorted image
        sobel = lines_pipe(unwarped, ksize=17, dir_thresh=(0.7, 1.3), sobel_thresh=(50, 80))
        # # apply color filters
        color_filters = color_pipe(unwarped, thresh=(230, 255))
        # # creates binary map of filter and color maps
        col_line_combined = np.zeros_like(sobel)
        col_line_combined[(sobel == 1) | (color_filters == 1)] = 1

        lines = fit_lines(col_line_combined, margin=150, minpix=20, nwindows=20)

        # Check if left line is close to previous frame's LEFT lane
        if self.polygon_points_old_left is None:
            self.polygon_points_old_left = lines[0]

        l_a = lines[0]
        l_b = self.polygon_points_old_left
        if cv2.matchShapes(l_a, l_b, 1, 0.0) < 0.35:
            self.polygon_points_old_left = lines[0]
        else:
            l_a = self.polygon_points_old_left

        # Check if left line is close to previous frame's RIGHT lane
        if self.polygon_points_old_right is None:
            self.polygon_points_old_right = lines[1]

        r_a = lines[1]
        r_b = self.polygon_points_old_right

        if cv2.matchShapes(r_a, r_b, 1, 0.0) < 0.35:
            self.polygon_points_old_right = lines[1]
        else:
            r_a = self.polygon_points_old_right

        if len(self.res_left) > 1:
            if lines[7] < np.percentile(self.res_left, 90):
                self.res_left = self.insert_new_chuck_one_out(self.res_left, lines[7], self.lag)
                self.left_lane = self.insert_new_chuck_one_out(self.left_lane, l_a, self.lag)
            if lines[8] < np.percentile(self.res_right, 90):
                self.res_right = self.insert_new_chuck_one_out(self.res_right, lines[8], self.lag)
                self.right_lane = self.insert_new_chuck_one_out(self.right_lane, r_a, self.lag)
        else:
            self.left_lane = self.insert_new_chuck_one_out(self.left_lane, l_a, self.lag)
            self.right_lane = self.insert_new_chuck_one_out(self.right_lane, r_a, self.lag)

        final_out = project_lanes_(col_line_combined, np.mean(self.left_lane, axis=0), np.mean(self.right_lane, axis=0), lines[2], dst, self.pts)

        self.left_lane_curvature = self.insert_new_chuck_one_out(self.left_lane_curvature, lines[3], self.lag * 10)
        self.right_lane_curvature = self.insert_new_chuck_one_out(self.right_lane_curvature, lines[3], self.lag * 10)

        self.position = (img.shape[1]/2 - np.mean((final_out[1], final_out[3]))) * 3.7 / 700

        if self.position >= 0:
            loc = ' right '
        else:
            loc = ' left '
        out = overlay_text(final_out[0], 'Left lane curvature radius: ' + str(round(np.mean(self.left_lane_curvature))) + 'm',
                           pos=(0, 0))
        out = overlay_text(out, 'Right lane curvature radius: ' + str(round(np.mean(self.right_lane_curvature))) + 'm',
                           pos=(0, 50))

        out = overlay_text(out, 'Average curvature radius: ' + str(round(np.mean([np.mean(self.left_lane_curvature),
                                                                                  np.mean(self.right_lane_curvature)]))) + 'm', pos=(0, 100))

        out = overlay_text(out, 'Vehicle position: ' + str(round(self.position, 3)) + loc + 'off centre',
                           pos=(0, 150))

        return out

# #
img = mpimg.imread('test_images/test4.jpg')
x = Pipes()

plt.imshow(x.full_pipe(img))
plt.savefig('images/img.png')
plt.show()