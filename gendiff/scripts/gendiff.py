"""
    gendiff -h
    usage: gendiff [-h] first_file second_file

    Compares two configuration files and shows a difference.

    positional arguments:
      first_file
      second_file

    optional arguments:
      -h, --help            show this help message and exit
"""

import argparse
from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')

    parser.add_argument('first_file', metavar='N', type=str)
    parser.add_argument('second_file', metavar='N', type=str)
    parser.add_argument('--format', metavar='N', type=str)

    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
