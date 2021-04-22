from argparse import ArgumentParser
from zfish_track.create_config import create_config
from zfish_track.run_tracking import run_tracking


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    create_config_parser = subparsers.add_parser('create-config', help="Create tracking configuration")
    create_config_parser.add_argument('input', nargs='*', default=None,
                                      help="Paths to videos or directories containing videos.")
    create_config_parser.add_argument('-d', '--directory', action='store_true',
                                      help="Select directories with GUI if no input is provided.")
    create_config_parser.add_argument('--same-config-for-each-directory', type=int, default=1,
                                      help="Create one config for all videos in each directory.")
    create_config_parser.add_argument('-r', '--recursive', action='store_true',
                                      help="Search for videos in all subdirectories.")
    create_config_parser.add_argument('-e', '--extension', nargs='*', default=['avi'],
                                      help="File extension for video (e.g., .avi) when searching for videos in "
                                           "directories.")
    create_config_parser.add_argument('--roi', nargs='*', type=int, default=True,
                                      help="ROI for tracking in the format of x0, y0, w, h. "
                                           "Set to True to select ROI using GUI.")
    create_config_parser.add_argument('--method', default='binary',
                                      help="Tracking method.")
    create_config_parser.add_argument('--interval', type=int, default=None,
                                      help='Interval in which tracking is done '
                                      '(e.g., "--interval 100, 200" to run tracking from frame 100 to 199). '
                                           'Whole video is tracked by default/')
    create_config_parser.add_argument('-v', '--verbose', type=int, default=0,
                                      help="Verbosity.")

    run_tracking_parser = subparsers.add_parser('run', help="Run tracking on tracking configurations.")
    run_tracking_parser.add_argument('input', nargs='*', default=None,
                                     help="Paths to tracking configurations or directories containing configurations.")
    run_tracking_parser.add_argument('-d', '--directory', action='store_true',
                                     help="Select directories with GUI if no input is provided.")
    run_tracking_parser.add_argument('-r', '--recursive', action='store_true',
                                     help="Search for videos in all subdirectories.")
    run_tracking_parser.add_argument('-v', '--verbose', type=int, default=0,
                                     help="Verbosity.")

    args = parser.parse_args()

    if args.command == 'create-config':
        create_config(args)
    elif args.command == 'run':
        run_tracking(args)


if __name__ == '__main__':
    main()
