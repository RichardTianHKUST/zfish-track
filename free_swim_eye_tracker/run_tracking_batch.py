import json
from pathlib import Path
from free_swim_eye_tracker.utils.io import ask_directory, ask_filenames
from free_swim_eye_tracker.utils.config import config_suffix, angles_suffix, points_suffix
from free_swim_eye_tracker.run_tracking import run_tracking
from free_swim_eye_tracker.utils.io import get_file


def run_tracking_on_videos(paths=None, skip_processed_videos=False):
    if paths is None:
        paths = ask_filenames()

    for path in paths:
        if skip_processed_videos:
            if str(path).endswith(config_suffix):
                with open(path, 'r') as f:
                    video_path = json.load(f)['video_path']
            else:
                video_path = path
            if Path(get_file(video_path, angles_suffix)).exists() and Path(get_file(video_path, points_suffix)).exists():
                print(str(video_path), 'has already been processed.')
                continue
        run_tracking(path)


def run_tracking_on_directory(directory=None, skip_processed_videos=False):
    if directory is None:
        directory = ask_directory()

    paths = list(Path(directory).glob(f'*{config_suffix}'))
    run_tracking_on_videos(paths, skip_processed_videos)


if __name__ == '__main__':
    run_tracking_on_directory()
