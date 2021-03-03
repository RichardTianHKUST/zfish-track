import cv2
from skimage.color import gray2rgb


contour_colors = [(31, 119, 180),
                  (255, 127, 14),
                  (44, 160, 44)
                  ]


def draw_results(src, contours=None, contour_thickness=-1):
    if len(src.shape) == 2:
        img = gray2rgb(src)
    else:
        img = src.copy()

    if contours is not None:
        for contour, color in zip(contours, contour_colors):
            cv2.drawContours(img, [contour], contourIdx=-1, color=color, thickness=contour_thickness)

    return img
