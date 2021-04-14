from argparse import ArgumentParser
from itertools import chain
from pathlib import Path
from zfish_track._gui import ParameterSelector
from zfish_track._io import ask_filenames, ask_directories


def create_config(args=None):
    if args is None:
        parser = ArgumentParser()
        parser.add_argument('input', nargs='*', default=None)
        parser.add_argument('-d', '--directory', action='store_true')
        parser.add_argument('--same-config-for-each-directory', type=int, default=1)
        parser.add_argument('-r', '--recursive', action='store_true')
        parser.add_argument('-e', '--extension', nargs='*', default=['avi'])
        parser.add_argument('--roi', nargs='*', type=int, default=True)
        parser.add_argument('--method', default='binary')
        parser.add_argument('--interval', type=int, default=None)
        parser.add_argument('-v', '--verbose', type=int, default=0)
        args = parser.parse_args()

    for i, extension in enumerate(args.extension):
        if not str(extension).startswith('.'):
            args.extension[i] = f'.{extension}'

    if len(args.input) == 0:
        if args.directory:
            args.input.extend(ask_directories())
        else:
            args.input.extend(ask_filenames())

    kwargs = dict(method=args.method, roi=args.roi, interval=args.interval, verbose=args.verbose)

    for path in args.input:
        path = Path(path)
        if path.is_dir():
            it = chain(*[path.rglob(f'*{extension}') if args.recursive else path.glob(f'*{extension}')
                         for extension in args.extension])

            if args.same_config_for_each_directory:
                config = ParameterSelector(next(it), **kwargs).get_config()
                for video_path in it:
                    config.save(video_path, verbose=args.verbose)
            else:
                for video_path in it:
                    ParameterSelector(video_path, **kwargs)
        else:
            if path.exists():
                ParameterSelector(path, **kwargs)


if __name__ == '__main__':
    create_config()
