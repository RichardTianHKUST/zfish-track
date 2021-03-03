import json
from pathlib import Path
from free_swim_eye_tracker.utils.io import ask_filename, get_file
from free_swim_eye_tracker.utils.config import config_suffix
from free_swim_eye_tracker.utils.tracking import track_video


def run_tracking(path=None):
    if path is None:
        path = ask_filename()

    if not str(path).endswith(config_suffix):
        path = get_file(path, config_suffix)

    if Path(path).exists():
        with open(path, 'r') as f:
            config = json.load(f)
            track_video(**config)


if __name__ == '__main__':
    run_tracking()
