#! /usr/bin/python3
import re
import argparse
import sys


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("regex_pattern", type=str, help="regex pattern")
    parser.add_argument('infile', nargs='*', type=argparse.FileType(mode='r', encoding='ascii'),
                        default=[sys.stdin], help="input files to search in")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--underscore", action='store_true', required=False,
                       help="print underscore under the matching text")
    group.add_argument("-c", "--color", action='store_true', required=False, help="highlight matching text")
    group.add_argument("-m", "--machine", action='store_true', required=False, help="generate machine readable output "
                                                                                    "format: "
                                                                                    "file_name:no_line:start_pos"
                                                                                    ":matched_text")
    args = parser.parse_args()
    return args


def find_match(args):
    filehandlers = args.infile
    regex = args.regex_pattern

    for filehandler in filehandlers:
        line = filehandler.readline().strip()
        line_number = 0
        while line:
            line_number += 1
            for match in re.finditer(regex, line):
                if args.underscore:
                    print_underscore(filehandler.name, line_number, match)
                elif args.color:
                    print_colored(filehandler.name, line_number, match)
                elif args.machine:
                    print_machine_format(filehandler.name, line_number, match)
                else:
                    print_matches(filehandler.name, line_number, match)
            line = filehandler.readline().strip()


def print_matches(filename, line_number, match):
    print(f"{filename} {line_number} {match.string}")


def print_underscore(filename, line_number, match):
    print(f"{filename} {line_number} {match.string}")
    amount_of_spaces = calc_underscore_start_position(filename, line_number, match.start())
    print(' ' * amount_of_spaces + "^")


def calc_underscore_start_position(filename, line_number, match_start_position):
    return len(filename) + 1 + len(str(line_number)) + 1 + match_start_position


def print_colored(filename, line_number, match):
    print(f"{filename} {line_number}", end=" ")
    line = match.string
    print(line[:match.start()] + '\033[0;36m' + match.group() + '\033[0;00m' + line[match.end():])


def print_machine_format(filename, line_number, match):
    print(f"{filename}:{line_number}:{match.start()}:{match.group()}")


def main():
    args = get_arguments()
    find_match(args)


if __name__ == "__main__":
    main()
