import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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


def dir_threshold(img, sobel_kernel=3, dir_thresh=(0.7, 1.3)):
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


def lines_pipe(image, ksize=25, sobel_thresh=(50, 180), mag_thresh_=(50, 110), dir_thresh=(0.7, 1.3)):
    """
    pipeline to use all the above filters
    :param image:
    :param ksize:
    :param sobel_thresh:
    :param mag_thresh_:
    :param dir_thresh:
    :return:
    """

    gradx = abs_sobel_thresh(image, orient='x', sobel_kernel=ksize, sobel_thresh=sobel_thresh)
    grady = abs_sobel_thresh(image, orient='y', sobel_kernel=ksize, sobel_thresh=sobel_thresh)

    mag_binary = mag_thresh(image, sobel_kernel=ksize, mag_thresh=mag_thresh_)

    dir_binary = dir_threshold(image, sobel_kernel=ksize, dir_thresh=dir_thresh)

    combined = np.zeros_like(dir_binary)
    combined[((gradx == 1)) | ((mag_binary == 1) & (dir_binary == 1))] = 1

    return combined

