import numpy as np
import cv2


def abs_sobel_thresh(img, orient='x', sobel_thresh=(0, 255),sobel_kernel=3):
    """
    returns gradient binaries
    :param img:
    :param orient:
    :param thresh_min:
    :param thresh_max:
    :return:
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    if orient == 'x':
        sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    else:
        sobel = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)

    sobel_abs = np.abs(sobel)
    scaled = np.uint8(255*sobel_abs/np.max(sobel_abs))
    sbinary = np.zeros_like(scaled)
    sbinary[(scaled >= sobel_thresh[0]) & (scaled <= sobel_thresh[1])] = 1

    return sbinary


def mag_thresh(img, sobel_kernel=3, mag_thresh=(0, 255)):
    """
    returns magnitude binaries
    :param img: image
    :param sobel_kernel:
    :param mag_thresh:
    :return:
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sobel_x = np.abs(cv2.Sobel(gray, cv2.CV_64F, ksize=sobel_kernel, dx=1, dy=0))
    sobel_y = np.abs(cv2.Sobel(gray, cv2.CV_64F, ksize=sobel_kernel, dx=0, dy=1))

    magnitude = (sobel_x**2 + sobel_y**2)**.5
    scaled_magnitude = np.uint8(255 * magnitude / np.max(magnitude))

    scaled_magnitude_bin = np.zeros_like(scaled_magnitude)
    scaled_magnitude_bin[(scaled_magnitude >= mag_thresh[0]) & (scaled_magnitude <= mag_thresh[1])] = 1

    return scaled_magnitude_bin


def dir_threshold(img, sobel_kernel=3, dir_thresh=(0, np.pi / 2)):
    """
    return direction binaries
    :param img:
    :param sobel_kernel:
    :param thresh:
    :return:
    """
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sobelx = np.absolute(cv2.Sobel(gray, cv2.CV_64F, ksize=sobel_kernel, dx=1, dy=0))
    sobely = np.absolute(cv2.Sobel(gray, cv2.CV_64F, ksize=sobel_kernel, dx=0, dy=1))
    gradient = np.arctan2(sobely, sobelx)
    binary_output = np.zeros_like(gradient)

    binary_output[(gradient >= dir_thresh[0]) & (gradient <= dir_thresh[1])] = 1

    return binary_output


def saturation(img, thresh=(170, 255)):
    img = np.copy(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HLS).astype(np.float)
    hsv_h = hsv[:, :, 0]
    hsv_s = hsv[:, :, 1]
    hsv_v = hsv[:, :, 2]
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float)
    hls_h = hls[:, :, 0]
    hls_l = hls[:, :, 1]
    hls_s = hls[:, :, 2]

    combined = np.zeros_like(hls_l)
    combined[(hsv_s >= thresh[0]) & (hsv_s < thresh[1]) |
             (hsv_v >= thresh[0]) & (hsv_v < thresh[1]) |
             (hls_l >= thresh[0]) & (hls_l < thresh[1]) |
             (hls_s >= thresh[0]) & (hls_s < thresh[1])] = 1


    return combined



def seeing_red(img, thresh=(180, 255)):
    img = np.copy(img)
    # Convert to HSV color space and separate the V channel
    red = img[:,:,0]
    combined = np.zeros_like(red)
    combined[(red >= thresh[0]) & (red < thresh[1])] = 1

    return combined


def thresh_pipe(img,ksize = 17):
    grad_x = abs_sobel_thresh(img, orient='x', sobel_kernel=ksize, sobel_thresh=(15, 100))
    sat = saturation(img, thresh=(240, 255))
    combined = np.zeros_like(sat)
    reds = seeing_red(img)
    combined[((reds == 1) | (sat == 1)) | (grad_x == 1)] = 1

    return combined

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
# plt.rcParams['image.cmap'] = 'gray'
# img = mpimg.imread('test_images/test5.jpg')
# plt.imshow(thresh_pipe(img))
# plt.show()
#
#

