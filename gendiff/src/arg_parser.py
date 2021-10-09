import argparse
import gendiff.src.constants as constants


def make_parser():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '--formatter',
        type=str,
        default=constants.FORMATTER_STYLISH,
        metavar='FORMATTER',
        help='set formatter of output'
    )
    parser.add_argument(
        '--f',
        '--format',
        type=str,
        metavar='FORMAT',
        help='set format of output'
    )

    return parser


def get_command_args():
    parser = make_parser()

    return parser.parse_args()
