import math
import warnings
import cv2
import numpy as np
import pandas as pd
from skimage.measure import EllipseModel


def radian(theta):
    return (theta + np.pi) % (np.pi * 2) - np.pi


def ccw_angle_between_vectors(v1, v2):
    return np.arcsin(np.cross(v1, v2) / np.linalg.norm(v1, axis=-1) / np.linalg.norm(v2, axis=-1))


def contour_centre(contour):
    moments = cv2.moments(contour)
    if moments['m00'] != 0:
        c = moments['m10'] / moments['m00'], moments['m01'] / moments['m00']
    else:
        c = np.mean(contour.reshape(-1, 2), axis=0)
    return c


def contour_angle(contour):
    moments = cv2.moments(contour)
    try:
        mu20 = moments['mu20'] / moments['m00']
        mu02 = moments['mu02'] / moments['m00']
        mu11 = moments['mu11'] / moments['m00']
    except ZeroDivisionError:
        return 0
    if (mu20 - mu02) != 0:
        theta = 0.5 * math.atan(2 * mu11 / (mu20 - mu02))
    else:
        theta = math.pi / 2
    return theta


def fit_ellipse(contour, use_convex_hull):
    if use_convex_hull:
        contour = cv2.convexHull(contour)

    cnt = contour.reshape(-1, 2) * 1.

    model = EllipseModel()

    try:
        assert model.estimate(cnt)
        return model.params
    except AssertionError:
        warnings.warn('ellipse model estimation failed')
        cx, cy = contour_centre(contour)
        angle = contour_angle(contour)
        a = b = np.linalg.norm(cnt.max(0) - cnt.min(0))
        return cx, cy, a, b, angle


def fit_ellipses(contours, use_convex_hull):
    ellipse_params = np.zeros((len(contours), 5))

    for i, contour in enumerate(contours):
        ellipse_params[i] = fit_ellipse(contour, use_convex_hull)

        if ellipse_params[i, 2] < ellipse_params[i, 3]:
            ellipse_params[i][[2, 3]] = ellipse_params[i][[3, 2]]
            ellipse_params[i, -1] = radian(ellipse_params[i, -1] - np.pi / 2)

    return ellipse_params


def correct_orientation(ellipse_params):
    try:
        assert len(ellipse_params) == 3
    except AssertionError:
        return ellipse_params

    dx, dy = ellipse_params[:2, :2].mean(0) - ellipse_params[-1, :2]
    orientation = np.arctan2(dy, dx)

    for i, ellipse_param in enumerate(ellipse_params):
        if abs(radian(orientation - ellipse_param[-1])) > np.pi / 2:
            ellipse_param[-1] = radian(ellipse_param[-1] - np.pi)

    return ellipse_params


def ellipse_points(params):
    orientations = params[:, -1]
    a = params[:, 2][..., None]
    v = a * np.stack([np.cos(orientations), np.sin(orientations)]).T
    center = params[:, :2]
    anterior = center + v
    posterior = center - v
    return anterior, center, posterior


def calculate_angles(df):
    vl = df['left_eye', 'anterior'] - df['left_eye', 'posterior']
    vr = df['right_eye', 'anterior'] - df['right_eye', 'posterior']
    vm = (df['left_eye', 'center'] + df['right_eye', 'center']) / 2 - df['swim_bladder', 'center']

    angle_l = ccw_angle_between_vectors(vm, vl)
    angle_r = ccw_angle_between_vectors(vr, vm)
    heading = np.arctan2(vm['y'], vm['x'])
    return np.rad2deg(pd.DataFrame({'left': angle_l, 'right': angle_r, 'heading': heading}))
