from argparse import ArgumentParser
from pathlib import Path
from zfish_track.gui import ParameterSelector
from zfish_track.io import ask_filenames, ask_directories


if __name__ == '__main__':
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

    video_paths = []

    for path in args.input:
        path = Path(path)
        if path.is_dir():
            for extension in args.extension:
                video_paths.extend(path.glob(('**/*' if args.recursive else '*') + extension))
        else:
            if path.exists():
                video_paths.append(path)

    for video_path in video_paths:
        ParameterSelector(video_path, roi=args.roi, method=args.method, interval=args.interval, verbose=args.verbose)
