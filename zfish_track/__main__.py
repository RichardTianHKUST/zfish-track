from argparse import ArgumentParser
from zfish_track.create_config import create_config
from zfish_track.run_tracking import run_tracking


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    create_config_parser = subparsers.add_parser('create-config')
    create_config_parser.add_argument('input', nargs='*', default=None)
    create_config_parser.add_argument('-d', '--directory', action='store_true')
    create_config_parser.add_argument('--same-config-for-each-directory', type=int, default=1)
    create_config_parser.add_argument('-r', '--recursive', action='store_true')
    create_config_parser.add_argument('-e', '--extension', nargs='*', default=['avi'])
    create_config_parser.add_argument('--roi', nargs='*', type=int, default=True)
    create_config_parser.add_argument('--method', default='binary')
    create_config_parser.add_argument('--interval', type=int, default=None)
    create_config_parser.add_argument('-v', '--verbose', type=int, default=0)

    run_tracking_parser = subparsers.add_parser('run')
    run_tracking_parser.add_argument('input', nargs='*', default=None)
    run_tracking_parser.add_argument('-d', '--directory', action='store_true')
    run_tracking_parser.add_argument('-r', '--recursive', action='store_true')
    run_tracking_parser.add_argument('-v', '--verbose', type=int, default=0)

    args = parser.parse_args()

    if args.command == 'create-config':
        create_config(args)
    elif args.command == 'run':
        run_tracking(args)


if __name__ == '__main__':
    main()
