import argparse
import gendiff.src.constants as constants


def make_parser():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument(
        '-f',
        '--format',
        default=constants.FORMAT_STYLISH,
        help='set format of output',
    )
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)

    return parser


def get_command_args():
    parser = make_parser()

    return parser.parse_args()
