from pathlib import Path
from typing import Union, Optional
import cv2
import numpy as np
from ._draw import draw_results
from ._segmentation import segmentation
from ._tracking import intermediate_tracking, preprocess_video
from ._config import TrackingConfiguration


class ParameterSelector:
    methods_params = {'binary': {'threshold': [173, 0, 255]}}

    def __init__(self, video_path: Union[str, Path], method: str = 'binary',
                 roi: Union[bool, tuple, list, np.ndarray, None] = True,
                 interval: Union[tuple, list, np.ndarray, None] = None, params: Optional[dict] = None,
                 verbose: int = 0):
        self.video_path = video_path
        self.method = method
        self.frames, self.roi = preprocess_video(video_path, roi, interval, verbose)
        self.interval = interval
        self.params = {param: default for param, (default, _, _) in self.methods_params[method].items()}

        if isinstance(params, dict):
            self.params.update(params)

        self.frame_pos = 0
        self.segmentation = segmentation
        self.window_name = 'Press Enter to save parameters'

        cv2.namedWindow(self.window_name)

        frame_bar_name = 'frame'
        cv2.createTrackbar(frame_bar_name, self.window_name, 0, len(self.frames) - 1, self.update_frame_bar)
        cv2.setTrackbarPos(frame_bar_name, self.window_name, self.frame_pos)

        for param, (_, low, high) in self.methods_params[method].items():
            cv2.createTrackbar(param, self.window_name, low, high, self.create_track_bar_callback(param))
            cv2.setTrackbarPos(param, self.window_name, self.params[param])

        self.update()

        key = None
        key_enter = 13
        key_esc = 27

        while key not in [key_enter, key_esc]:
            key = cv2.waitKey()

        cv2.destroyAllWindows()

        if key == key_enter:
            self.get_config().save(verbose=verbose)

    def get_config(self):
        return TrackingConfiguration(self.video_path, self.method, self.roi, self.interval, self.params)

    def create_track_bar_callback(self, track_bar_name):
        return lambda value: self.update_parameter(track_bar_name, value)

    def update_parameter(self, name, value):
        self.params[name] = value
        self.update()

    def update_frame_bar(self, frame_pos):
        self.frame_pos = frame_pos
        self.update()

    def image_func(self, img):
        sorted_contours, eye_points = intermediate_tracking(img, self.method, self.params)
        return draw_results(img, sorted_contours, eye_points)

    def update(self):
        img = self.image_func(self.frames[self.frame_pos])
        cv2.imshow(self.window_name, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
