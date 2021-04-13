import json
from argparse import ArgumentParser
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


def run_tracking_on_directory(directory=None, skip_processed_videos=False, recursive=False):
    if directory is None:
        directory = ask_directory()
    directory = Path(directory)
    paths = list(directory.rglob(f'*{config_suffix}') if recursive else directory.glob(f'*{config_suffix}'))
    run_tracking_on_videos(paths, skip_processed_videos)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('directory', nargs='?', help="directory", default=None)
    parser.add_argument('--skip-processed-videos', help="skip processed videos", action='store_true')
    parser.add_argument('-r', '--recursive', help="search for files in the subdirectories", action='store_true')
    run_tracking_on_directory(**vars(parser.parse_args()))
