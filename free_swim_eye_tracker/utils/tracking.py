import numpy as np
import pandas as pd
from .geometry import calculate_angles, fit_ellipses, ellipse_points, correct_orientation
from .image_processing import imcrop, read_video, white_on_black
from .io import get_file
from .segmentation import segmentation
from .config import points_suffix, angles_suffix
from .contours import find_contours, sort_contours


def preprocess_video(video_path, roi):
    frames = white_on_black(read_video(video_path, as_gray=True))
    frames, roi = imcrop(frames, roi)
    return frames, roi


def intermediate_tracking(img, method, params):
    thresh = segmentation(img, method, params)
    contours = find_contours(thresh)
    sorted_contours = sort_contours(contours)
    ellipses = fit_ellipses(sorted_contours, use_convex_hull=True)
    ellipses = correct_orientation(ellipses)
    eye_points = ellipse_points(ellipses)
    return sorted_contours, eye_points


def track_video(video_path, roi, method, params):
    frames, roi = preprocess_video(video_path, roi=roi)
    eye_points = np.array([intermediate_tracking(frame, method, params)[1] for frame in frames]) + roi[:2]
    columns = pd.MultiIndex.from_product([['anterior', 'center', 'posterior'],
                                          ['left_eye', 'right_eye', 'swim_bladder'],
                                          ['x', 'y']])
    df_points = pd.DataFrame(eye_points.reshape(-1, 18), columns=columns).swaplevel(i=0, j=1, axis=1).sort_index(axis=1)
    df_angles = calculate_angles(df_points)
    df_points.to_csv(get_file(video_path, points_suffix))
    df_angles.to_csv(get_file(video_path, angles_suffix))
