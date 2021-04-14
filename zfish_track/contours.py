import warnings
import cv2
import numpy as np
from .geometry import ccw_angle_between_vectors


def find_contours(img: np.ndarray):
    return cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]


def sort_contours(contours: list):
    largest3 = sorted(contours, key=cv2.contourArea)[-3:]

    try:
        assert len(largest3) == 3
    except AssertionError:
        warnings.warn('Less than 3 contours detected. Try changing the parameters.')
        return largest3

    centers = np.array([contour.mean(0)[0] for contour in largest3])
    swim_bladder = int(np.argmin([np.linalg.norm(np.subtract(*centers[np.delete(np.arange(3), i)])) for i in range(3)]))
    eyes = np.delete(np.arange(3), swim_bladder)
    eyes_centers = centers[eyes]
    midpoint = eyes_centers.mean(axis=0)
    v_eyes = np.subtract(*eyes_centers)
    v_mid = centers[swim_bladder] - midpoint
    right = eyes[int(ccw_angle_between_vectors(v_mid, v_eyes) > 0)]
    left = np.delete(np.arange(3), [right, swim_bladder])[0]

    return largest3[left], largest3[right], largest3[swim_bladder]
