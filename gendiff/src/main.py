import argparse


def make_parser():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)

    return parser


def run():
    parser = make_parser()
    parser.parse_args()
