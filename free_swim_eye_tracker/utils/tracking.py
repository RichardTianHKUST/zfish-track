from pathlib import Path
import numpy as np
import pandas as pd
from .geometry import calculate_angles, fit_ellipses, ellipse_points, correct_orientation
from .image_processing import imcrop, read_video, white_on_black
from .io import get_file
from .segmentation import segmentation
from .config import points_suffix, angles_suffix
from .contours import find_contours, sort_contours


def preprocess_video(video_path, roi, interval):
    frames = white_on_black(read_video(video_path, as_gray=True))
    try:
        interval = (0 if interval[0] is None else interval[0], len(frames) if interval[1] is None else interval[1])
    except IndexError:
        interval = (0, len(frames))
    frames = frames[interval[0]:interval[1]]
    frames, roi = imcrop(frames, roi)
    return frames, roi, interval


def intermediate_tracking(img, method, params):
    thresh = segmentation(img, method, params)
    contours = find_contours(thresh)
    sorted_contours = sort_contours(contours)
    ellipses = fit_ellipses(sorted_contours, use_convex_hull=True)
    ellipses = correct_orientation(ellipses)
    eye_points = ellipse_points(ellipses)
    return sorted_contours, eye_points


def track_video(video_path, roi, method, params, interval=None):
    frames, roi, interval = preprocess_video(video_path, roi=roi, interval=interval)
    eye_points = np.array([intermediate_tracking(frame, method, params)[1] for frame in frames]) + roi[:2]
    columns = pd.MultiIndex.from_product([['anterior', 'center', 'posterior'],
                                          ['left_eye', 'right_eye', 'swim_bladder'],
                                          ['x', 'y']])

    index = pd.Index(np.arange(*interval))
    df_points_new = pd.DataFrame(eye_points.reshape(-1, 18),
                                 columns=columns, index=index).swaplevel(i=0, j=1, axis=1).sort_index(axis=1)
    df_angles_new = calculate_angles(df_points_new)
    df_angles_new.index = index

    path_points = get_file(video_path, points_suffix)
    path_angles = get_file(video_path, angles_suffix)

    if Path(path_points).exists():
        df_points = pd.read_csv(path_points, index_col=0, header=[0, 1, 2])
        for i in range(*interval):
            df_points.loc[i] = df_points_new.loc[i]
    else:
        df_points = df_points_new

    if Path(path_angles).exists():
        df_angles = pd.read_csv(path_angles, index_col=0)
        for i in range(*interval):
            df_angles.loc[i] = df_angles_new.loc[i].values
    else:
        df_angles = df_angles_new

    df_points.sort_index(axis=0).to_csv(path_points)
    df_angles.sort_index(axis=0).to_csv(path_angles)
