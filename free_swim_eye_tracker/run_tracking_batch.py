from pathlib import Path
from free_swim_eye_tracker.utils.io import ask_directory, ask_filenames
from free_swim_eye_tracker.utils.config import config_suffix
from free_swim_eye_tracker.run_tracking import run_tracking


def run_tracking_on_videos(paths=None):
    if paths is None:
        paths = ask_filenames()

    for path in paths:
        run_tracking(path)


def run_tracking_on_directory(directory=None):
    if directory is None:
        directory = ask_directory()

    paths = list(Path(directory).glob(f'*{config_suffix}'))
    run_tracking_on_videos(paths)


if __name__ == '__main__':
    run_tracking_on_directory()
