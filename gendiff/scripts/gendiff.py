#!/usr/bin/env python
from gendiff.src.arg_parser import get_command_args
from gendiff import generate_diff


def main():
    args = get_command_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)


if __name__ == '__main__':
    main()
