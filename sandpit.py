import pickle
import cv2

with open(r'camera_cal/wide_dist_pickle.p', 'rb') as pickle_file:
    p = pickle.load(pickle_file)

mtx = p['mtx']
dist = p['dist']