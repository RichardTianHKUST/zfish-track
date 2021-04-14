import cv2
import numpy as np
from skimage.color import gray2rgb

contour_colors = [(31, 119, 180),
                  (255, 127, 14),
                  (44, 160, 44)]


def draw_results(src, contours=None, eye_points=None, contour_thickness=-1):
    if len(src.shape) == 2:
        img = gray2rgb(src)
    else:
        img = src.copy()

    if contours is not None:
        for contour, color in zip(contours, contour_colors):
            cv2.drawContours(img, [contour], contourIdx=-1, color=color, thickness=contour_thickness)

    if eye_points is not None:
        anterior, center, posterior = np.array(eye_points).astype(int)
        for c, a in zip(center, anterior):
            cv2.line(img, tuple(c), tuple((a - c) * 2 + c), (0, 255, 255), 1)

    return img
