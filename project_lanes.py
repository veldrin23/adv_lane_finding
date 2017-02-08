import numpy as np
import cv2

def project_lanes_(warped, left_fitx, right_fitx, ploty, original_image, src):
    src = np.float32(src)
    dst = np.float32([(0, 720), (0, 0), (1280, 0), (1280, 720)])
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))



    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    # newwarp = cv2.warpPerspective(color_warp, Minv, (original_image.shape[1], original_image.shape[0]))
    m = cv2.getPerspectiveTransform(dst, src)
    undist = cv2.warpPerspective(color_warp, m, None)
    green_blob = np.where(undist[:, :, 1] != 0)
    bot_left = np.min(green_blob[1])
    bot_right = np.max(green_blob[1])

    top_left = np.min(green_blob[1][green_blob[0] == np.min(green_blob[0])])
    top_right = np.max(green_blob[1][green_blob[0] == np.min(green_blob[0])])
    # print(min_x, max_x)
    # Combine the result with the original image
    result = cv2.addWeighted(original_image, 1, undist, 0.2, 0)

    return result, bot_left, top_left,  top_right, bot_right

