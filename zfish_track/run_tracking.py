import json
import logging
from argparse import ArgumentParser
from pathlib import Path
from zfish_track._io import ask_filenames, ask_directories
from zfish_track._config import config_suffix
from zfish_track._tracking import track_video


def run_tracking(args=None):
    if args is None:
        parser = ArgumentParser()
        parser.add_argument('input', nargs='*', default=None)
        parser.add_argument('-d', '--directory', action='store_true')
        parser.add_argument('-r', '--recursive', action='store_true')
        parser.add_argument('-v', '--verbose', type=int, default=0)
        args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    if len(args.input) == 0:
        if args.directory:
            args.input.extend(ask_directories())
        else:
            args.input.extend(ask_filenames())

    config_paths = []

    for path in args.input:
        path = Path(path)
        if path.is_dir():
            config_paths.extend(path.glob(('**/*' if args.recursive else '*') + config_suffix))
        else:
            if path.exists():
                if str(path).endswith(config_suffix):
                    config_paths.append(path)

    for config_path in config_paths:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            track_video(**config, verbose=args.verbose)
        except Exception as error:
            logger.exception(error)


if __name__ == '__main__':
    run_tracking()
