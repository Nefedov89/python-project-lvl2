import argparse


def make_parser():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '--f',
        '--format',
        metavar='FORMAT',
        help='set format of output'
    )

    return parser


def get_command_args():
    parser = make_parser()

    return parser.parse_args()
