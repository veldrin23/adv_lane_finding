import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def color_pipe(img, thresh=(230, 255)):
    img = np.copy(img)
    # Convert to HSV color space and separate the V channel
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HLS).astype(np.float)
    hsv_s = hsv[:, :, 1]
    hsv_v = hsv[:, :, 2]
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float)
    hls_l = hls[:, :, 1]
    hls_s = hls[:, :, 2]

    combined = np.zeros_like(hls_l)
    combined[(hsv_s >= thresh[0]) & (hsv_s < thresh[1]) |
             (hsv_v >= thresh[0]) & (hsv_v < thresh[1]) |
             (hls_l >= thresh[0]) & (hls_l < thresh[1]) |
             (hls_s >= thresh[0]) & (hls_s < thresh[1])] = 1

    # yellow
    yellow = cv2.inRange(hsv, (20, 100, 100), (50, 255, 255))

    # white
    sensitivity_1 = 68
    white = cv2.inRange(hsv, (0, 0, 255 - sensitivity_1), (255, 20, 255))

    sensitivity_2 = 60
    HSL = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    white_2 = cv2.inRange(HSL, (0, 255 - sensitivity_2, 0), (255, 255, sensitivity_2))
    white_3 = cv2.inRange(img, (200, 200, 200), (255, 255, 255))

    colors_bin = yellow | white | white_2 | white_3
    colors_bin = np.divide(colors_bin, 255)
    zeros = np.zeros_like(colors_bin)
    zeros[(colors_bin == 1) | (combined == 1)] = 1
    return zeros




"""
HSV = cv2.cvtColor(your_image, cv2.COLOR_RGB2HSV)

# For yellow
yellow = cv2.inRange(HSV, (20, 100, 100), (50, 255, 255))

# For white
sensitivity_1 = 68
white = cv2.inRange(HSV, (0,0,255-sensitivity_1), (255,20,255))

sensitivity_2 = 60
HSL = cv2.cvtColor(your_image, cv2.COLOR_RGB2HLS)
white_2 = cv2.inRange(HSL, (0,255-sensitivity_2,0), (255,255,sensitivity_2))
white_3 = cv2.inRange(your_image, (200,200,200), (255,255,255))

bit_layer = your_bit_layer | yellow | white | white_2 | white_3

"""