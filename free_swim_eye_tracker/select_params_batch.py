from pathlib import Path
from free_swim_eye_tracker.utils.config import config_suffix
from free_swim_eye_tracker.utils.io import ask_directory, ask_filenames, get_file
from free_swim_eye_tracker.select_params import ParameterSelector


def batch_select_parameters_from_videos(video_paths=None, method='binary', roi=True, start_from_prev_params=True,
                                        skip_processed_videos=False):
    if video_paths is None:
        video_paths = ask_filenames()
    prev_params = {}
    for video_path in video_paths:
        if skip_processed_videos:
            if get_file(video_path, config_suffix).exists():
                continue
        selector = ParameterSelector(video_path, roi, method=method, params=prev_params)
        if start_from_prev_params:
            prev_params.update(selector.params)


def batch_select_parameters_from_directory(directory=None, video_extension='.avi', method='binary', roi=True,
                                           start_from_prev_params=True, skip_processed_videos=False):
    if directory is None:
        directory = ask_directory()

    video_paths = list(Path(directory).glob(f'*{video_extension}'))
    batch_select_parameters_from_videos(video_paths, method, roi, start_from_prev_params, skip_processed_videos)


if __name__ == '__main__':
    batch_select_parameters_from_directory()
