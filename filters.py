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


def seeing_red(img, thresh=(0,255)):
    red = img[:, :, 0]

    r_binary = np.zeros_like(red)
    r_binary[((red > thresh[0]) & (red < thresh[1]))] = 1

    return r_binary


def saturation_thresh(img, thresh=(0,255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float)
    hls_s = hls[:, :, 2]

    sat_binary = np.zeros_like(hls_s)
    sat_binary[(sat_binary > thresh[0]) & (sat_binary < thresh[1])] = 1

    return sat_binary


def filters_pipeline(img, ksize=17):
    gradx = abs_sobel_thresh(img, orient='x', sobel_kernel=ksize, sobel_thresh=(15, 100))
    saturation = saturation_thresh(img, thresh=(230, 255))
    reds = seeing_red(img, thresh=(230, 255))

    combined = np.zeros_like(saturation)
    combined[((reds == 1) | (saturation == 1)) | (gradx == 1)] = 1

    return combined
