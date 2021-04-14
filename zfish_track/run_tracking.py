import json
import logging
from argparse import ArgumentParser
from pathlib import Path
from zfish_track.io import ask_filenames, ask_directory
from zfish_track.config import config_suffix
from zfish_track.tracking import track_video


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    parser = ArgumentParser()
    parser.add_argument('input', nargs='*', default=None)
    parser.add_argument('-d', '--directory', action='store_true')
    parser.add_argument('-r', '--recursive', action='store_true')
    args = parser.parse_args()

    if len(args.input) == 0:
        if args.directory:
            args.input.append(ask_directory())
        else:
            args.input.extend(ask_filenames())

    config_paths = []

    for path in args.input:
        path = Path(path)
        if path.is_dir():
            config_paths.extend(path.glob(('**/' if args.recursive else '') + config_suffix))
        else:
            if path.exists():
                if str(path).endswith(config_suffix):
                    config_paths.append(path)

    for config_path in config_paths:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            track_video(**config)
        except Exception as error:
            logger.exception(error)
