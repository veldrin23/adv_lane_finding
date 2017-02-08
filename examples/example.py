import cv2
import numpy as np

def warper(img, src, dst):

    # Compute and apply perpective transform
    img_size = (img.shape[1], img.shape[0])
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_NEAREST)  # keep same size as input image

    return warped


class Line():
    def __init__(self):
        # was the line detected in the last iteration?
        self.detected = False
        # x values of the last n fits of the line
        self.recent_xfitted = []
        #average x values of the fitted line over the last n iterations
        self.bestx = 'asd'
        #polynomial coefficients averaged over the last n iterations
        self.best_fit = None
        #polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]
        #radius of curvature of the line in some units
        self.radius_of_curvature = None
        #distance in meters of vehicle center from the line
        self.line_base_pos = None
        #difference in fit coefficients between last and new fits
        self.diffs = np.array([0,0,0], dtype='float')
        #x values for detected line pixels
        self.allx = None
        #y values for detected line pixels
        self.ally = None

x = Line
print(x.bestx)

# # Create an image to draw the lines on
# warp_zero = np.zeros_like(warped).astype(np.uint8)
# color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
#
# # Recast the x and y points into usable format for cv2.fillPoly()
# pts_left = np.array([np.transpose(np.vstack([left_fitx, yvals]))])
# pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, yvals])))])
# pts = np.hstack((pts_left, pts_right))
#
# # Draw the lane onto the warped blank image
# cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))
#
# # Warp the blank back to original image space using inverse perspective matrix (Minv)
# newwarp = cv2.warpPerspective(color_warp, Minv, (image.shape[1], image.shape[0]))
# # Combine the result with the original image
# result = cv2.addWeighted(undist, 1, newwarp, 0.3, 0)
# plt.imshow(result)


def __draw_colored_fill(self, img, offset, pts):
    """
    Draws a cv2.fillPoly that is colored according to how far it is away from the
    center of the lane. Good for drivers to see how safe autonomous driving is!
    """
    limits = [0.35, 0.65]
    scale_factor = 255 / ((limits[1] - limits[0]) / 2)
    mid = (limits[0] + limits[1]) / 2

    if offset < mid:
        r = scale_factor * (offset - limits[0])
        cv2.fillPoly(img, np.int_([pts]), (r, 255, 0))

    elif (offset > mid) & (offset < limits[1]):
        g = scale_factor * (limits[1] - offset)
        cv2.fillPoly(img, np.int_([pts]), (255, g, 0))
    else:
        cv2.fillPoly(img, np.int_([pts]), (255, 0, 0))

    return img