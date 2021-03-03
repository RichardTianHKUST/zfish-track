import numpy as np
import pandas as pd
from skimage.measure import EllipseModel


def radian(theta):
    return (theta + np.pi) % (np.pi * 2) - np.pi


def ccw_angle_between_vectors(v1, v2):
    return np.arcsin(np.cross(v1, v2) / np.linalg.norm(v1, axis=-1) / np.linalg.norm(v2, axis=-1))


def fit_ellipses(contours):
    ellipse_params = np.zeros((len(contours), 5))

    for i, contour in enumerate(contours):
        model = EllipseModel()
        assert model.estimate(contour.reshape(-1, 2) * 1.)
        ellipse_params[i] = model.params

        if ellipse_params[i, 2] < ellipse_params[i, 3]:
            ellipse_params[i][[2, 3]] = ellipse_params[i][[3, 2]]
            ellipse_params[i, -1] = radian(ellipse_params[i, -1] - np.pi / 2)

    return ellipse_params


def correct_orientation(ellipse_params):
    assert len(ellipse_params) == 3
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
