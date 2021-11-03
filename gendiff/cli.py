#!/usr/bin/env python
from gendiff.src.arg_parser import get_command_args
from gendiff import generate_diff
import gendiff.src.constants as constants


def main():
    args = get_command_args()
    output_format = args.format\
        if args.format is not None\
        else constants.FORMAT_STYLISH

    diff = generate_diff(
        file1=args.first_file,
        file2=args.second_file,
        output_format=output_format
    )
    print(diff)


if __name__ == '__main__':
    main()
