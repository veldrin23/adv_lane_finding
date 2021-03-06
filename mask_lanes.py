import numpy as np
import cv2
import matplotlib.pyplot as plt



def fit_lines(binary_warped, margin = 100, minpix= 50, nwindows = 9):

    # Assuming you have created a warped binary image called "binary_warped"
    # Take a histogram of the bottom half of the image
    histogram = np.sum(binary_warped[int(binary_warped.shape[0]/3):,:], axis=0)
    # Create an output image to draw on and  visualize the result
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int(histogram.shape[0]/2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    # Choose the number of sliding windows
    # Set height of windows
    window_height = np.int(binary_warped.shape[0]/nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Current positions to be updated for each window
    leftx_current = leftx_base
    rightx_current = rightx_base
    # Set the width of the windows +/- margin
    # Set minimum number of pixels found to recenter window
    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_warped.shape[0] - (window + 1) * window_height
        win_y_high = binary_warped.shape[0] - window * window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        # Draw the windows on the visualization image
        cv2.rectangle(out_img, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), (0, 255, 0), 2)
        cv2.rectangle(out_img, (win_xright_low, win_y_low), (win_xright_high, win_y_high), (0, 255, 0), 2)
        # Identify the nonzero pixels in x and y within the window
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (
        nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (
        nonzerox < win_xright_high)).nonzero()[0]
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]


    # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2, full=True)
    right_fit = np.polyfit(righty, rightx, 2, full=True)


    ploty = np.linspace(0, binary_warped.shape[0] - 1, binary_warped.shape[0], dtype=int)

    left_fitx = left_fit[0][0] * ploty ** 2 + left_fit[0][1] * ploty + left_fit[0][2]
    right_fitx = right_fit[0][0] * ploty ** 2 + right_fit[0][1] * ploty + right_fit[0][2]

    # curvture
    y_eval = np.max(ploty)
    # Define conversions in x and y from pixels space to meters
    ym_per_pix = 30 / 720  # meters per pixel in y dimension
    xm_per_pix = 3.7 / 700  # meters per pixel in x dimension
    # Fit new polynomials to x,y in world space
    left_fit_cr = np.polyfit(ploty * ym_per_pix, left_fitx * xm_per_pix, 2)
    right_fit_cr = np.polyfit(ploty * ym_per_pix, right_fitx * xm_per_pix, 2)
    # Calculate the new radii of curvature
    left_curverad = ((1 + (2 * left_fit_cr[0] * y_eval * ym_per_pix + left_fit_cr[1]) ** 2) ** 1.5) / np.absolute(
        2 * left_fit_cr[0])
    right_curverad = ((1 + (2 * right_fit_cr[0] * y_eval * ym_per_pix + right_fit_cr[1]) ** 2) ** 1.5) / np.absolute(
        2 * right_fit_cr[0])

    if left_fit[0][0] <= 0:
        left_lane_dir = 'Left'
    else:
        left_lane_dir = 'Right'

    if right_fit[0][0] <= 0:
        right_lane_dir = 'Left'
    else:
        right_lane_dir = 'Right'

    res_left = left_fit[1]
    res_right = right_fit[1]


    return left_fitx, right_fitx, ploty, left_curverad, right_curverad, left_lane_dir, right_lane_dir, res_left, res_right





# original, which i tried to do myself..
"""


def mask_lanes(img, steps=20, lane_width=50, peak_thresh=(80,250)):

    mask = np.zeros_like(img)

    img_h = img.shape[0]
    img_w = img.shape[1]


    for s in range(steps):
        # left
        hist_left = np.sum(img[int((img_h - img_h/steps*(s+1))):
                               int((img_h - img_h/steps*s)),
                               0:int(img_w/2)], axis=0)
        peaks_left = find_peaks_cwt(hist_left, np.arange(peak_thresh[0], peak_thresh[1]))

        if len(peaks_left) > 0:
            mask[int((img_h - img_h/steps*(s+1))): int((img_h - img_h/steps*s)), peaks_left[0] - int(lane_width/2): peaks_left[0] + int(lane_width/2)] = 1

        # right
        hist_right = np.sum(img[int((img_h - img_h / steps * (s + 1))):
        int((img_h - img_h / steps * s)),
                           int(img_w / 2):], axis=0)
        peaks_right = find_peaks_cwt(hist_right, np.arange(peak_thresh[0], peak_thresh[1]))

        if len(peaks_right) > 0:
            mask[int((img_h - img_h / steps * (s + 1))): int((img_h - img_h / steps * s)),
            peaks_right[0] + int((img_w - lane_width) / 2) : peaks_right[0] + int((img_w + lane_width) / 2)] = 1

    return mask
"""
