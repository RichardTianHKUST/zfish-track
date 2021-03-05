from typing import Union
import json
from pathlib import Path
import cv2
from free_swim_eye_tracker.utils.draw import draw_results
from free_swim_eye_tracker.utils.io import ask_filename, get_file
from free_swim_eye_tracker.utils.segmentation import segmentation
from free_swim_eye_tracker.utils.tracking import intermediate_tracking, preprocess_video
from free_swim_eye_tracker.utils.config import config_suffix


class ParameterSelector:
    methods_params = {'binary': {'threshold': [173, 0, 255]}}

    def __init__(self, video_path=None, roi: Union[bool, list] = True, method='binary', params=None):
        if video_path is None:
            video_path = ask_filename()

        self.video_path = str(video_path)
        self.frames, self.roi = preprocess_video(video_path, roi)
        self.method = method
        self.frame_pos = 0
        self.segmentation = segmentation
        self.window_name = 'Press Enter to save parameters'

        cv2.namedWindow(self.window_name)

        frame_bar_name = 'frame'
        cv2.createTrackbar(frame_bar_name, self.window_name, 0, len(self.frames) - 1, self.update_frame_bar)
        cv2.setTrackbarPos(frame_bar_name, self.window_name, self.frame_pos)

        self.params = {param: default for param, (default, _, _) in self.methods_params[self.method].items()}

        if isinstance(params, dict):
            self.params.update(params)

        for param, (_, low, high) in self.methods_params[self.method].items():
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
            config = {'video_path': Path(self.video_path).absolute().as_posix(),
                      'roi': self.roi, 'method': self.method, 'params': self.params}
            with open(get_file(self.video_path, config_suffix), 'w') as f:
                json.dump(config, f)

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


if __name__ == '__main__':
    ParameterSelector()
