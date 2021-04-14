import cv2
import numpy as np
from imageio import get_reader


def read_video(path, as_gray, verbose=0):
    if verbose:
        print(f'Reading {path}')
    frames = np.array([i for i in get_reader(path)])
    if as_gray and len(frames.shape) == 4:
        return frames[..., 0]
    return frames


def white_on_black(img):
    if np.mean(img) >= 128:
        return 255 - img

    return img


def imcrop(img, roi=True, func=np.max):
    if roi is True:
        window_name = 'Select ROI'
        proj = func(img, axis=tuple(np.arange(len(img.shape))[:-2]))
        roi = cv2.selectROI(windowName=window_name, img=proj)
        cv2.destroyWindow(window_name)
    elif roi is False:
        roi = None

    if isinstance(roi, (tuple, list, np.ndarray)):
        img = img[..., roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

    return img, roi
