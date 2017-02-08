import pickle
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


with open(r'camera_cal/wide_dist_pickle.p', 'rb') as pickle_file:
    p = pickle.load(pickle_file)

mtx = p['mtx']
dist = p['dist']

img = mpimg.imread('camera_cal/calibration5.jpg')
plt.imshow(img)
plt.savefig('images/cal5.png')
dst = cv2.undistort(img, mtx, dist)

plt.imshow(dst)
plt.savefig('images/undist2.png')


