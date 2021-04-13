import json
import warnings
from argparse import ArgumentParser
from pathlib import Path
from glob import glob
from free_swim_eye_tracker.utils.io import ask_filename
from free_swim_eye_tracker.utils.config import config_suffix
from free_swim_eye_tracker.utils.tracking import track_video


def run_tracking(path=None):
    if path is None:
        path = ask_filename()

    if not str(path).endswith(config_suffix):
        paths = glob(Path(path).with_suffix('').as_posix() + '*' + config_suffix)
        if len(paths) == 0:
            warnings.warn(path + ' has not been created. Run parameter selection first.')
        else:
            for path in paths:
                run_tracking(path)

    if Path(path).exists():
        with open(path, 'r') as f:
            config = json.load(f)
            try:
                track_video(**config)
            except Exception as e:
                warnings.warn(f'Error encountered while processing {path}:' + str(e))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path', nargs='?', help='video path', default=None)
    run_tracking(**parser.parse_args().__dict__)
