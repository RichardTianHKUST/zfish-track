import cv2
import numpy as np
from tqdm import tqdm


def read_video(path, as_gray, verbose=0):
    if verbose:
        print(f'Reading {path}')

    cap = cv2.VideoCapture(str(path))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    range_ = tqdm(range(frame_count)) if verbose else range(frame_count)

    if as_gray:
        frames = np.array([cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY) for _ in range_])
    else:
        frames = np.array([cap.read()[1] for _ in range_])

    cap.release()

    return frames


def white_on_black(img):
    if np.mean(img) >= 128:
        return 255 - img

    return img


def imcrop(img, roi=True, func=np.max, verbose=0):
    if roi is True:
        window_name = 'Select ROI'
        proj = func(img, axis=tuple(np.arange(len(img.shape))[:-2]))
        roi = cv2.selectROI(windowName=window_name, img=proj)
        cv2.destroyWindow(window_name)
        if verbose:
            print(f'Selected ROI: {roi}')
    elif roi is False:
        roi = None

    if isinstance(roi, (tuple, list, np.ndarray)):
        img = img[..., roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

    return img, roi
