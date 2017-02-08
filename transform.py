import cv2
import numpy as np


def unwarp(img, src=((0, 720), (580, 450), (700, 450), (1280, 720))):
    src = np.float32(src)
    dst = np.float32([(0, 720), (0, 0), (1280, 0), (1280, 720)])
    m = cv2.getPerspectiveTransform(src, dst)
    undist = cv2.warpPerspective(img, m, None)
    return undist

