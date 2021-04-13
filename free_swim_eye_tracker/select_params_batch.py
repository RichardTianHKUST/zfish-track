from argparse import ArgumentParser
from pathlib import Path
from free_swim_eye_tracker.utils.config import config_suffix
from free_swim_eye_tracker.utils.io import ask_directory, ask_filenames, get_file
from free_swim_eye_tracker.select_params import ParameterSelector


def batch_select_parameters_from_videos(video_paths=None, method='binary', roi=True, start_from_prev_params=True,
                                        start_from_prev_roi=False, skip_processed_videos=False, use_same_config=False):
    if use_same_config:
        start_from_prev_params = True
        start_from_prev_roi = True
    if video_paths is None:
        video_paths = ask_filenames()
    prev_params = {}
    for i, video_path in enumerate(video_paths):
        if skip_processed_videos:
            if Path(get_file(video_path, config_suffix)).exists():
                continue
        selector = ParameterSelector(video_path, roi, method=method, params=prev_params,
                                     skip_gui=use_same_config and (i != 0))
        if start_from_prev_params:
            prev_params.update(selector.params)
        if start_from_prev_roi:
            roi = selector.roi


def batch_select_parameters_from_directory(directory=None, video_extension='.avi', method='binary', roi=True,
                                           start_from_prev_params=True, start_from_prev_roi=False,
                                           skip_processed_videos=False, use_same_config=False, recursive=False):
    if directory is None:
        directory = ask_directory()
    directory = Path(directory)
    video_paths = list(directory.rglob(f'*{video_extension}') if recursive else directory.glob(f'*{video_extension}'))
    batch_select_parameters_from_videos(video_paths, method, roi, start_from_prev_params,
                                        start_from_prev_roi, skip_processed_videos, use_same_config)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('directory', nargs='?', default=None)
    parser.add_argument('-e', '--extension', help="file extension for videos", default='.avi')
    parser.add_argument('-m', '--method', help="tracking method", default='binary')
    parser.add_argument('--roi', nargs='*', default=True, type=int)
    parser.add_argument('--start-from-prev-roi', help='use the same ROI for all videos', action='store_true')
    parser.add_argument('--skip-processed-video', help='skip processed video', action='store_true')
    parser.add_argument('-u', '--use-same-config', help='generate the same config for all videos', action='store_true')
    parser.add_argument('-r', '--recursive', help="search for files in the subdirectories", action='store_true')
    batch_select_parameters_from_directory(**vars(parser.parse_args()))
