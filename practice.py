#! /usr/bin/python3
import re
import argparse
import os.path
import sys


def get_arguments():
    # filename = sys.argv[1]
    # regex = sys.argv[2]
    # return filename, regex
    parser = argparse.ArgumentParser()
    parser.add_argument("regex_pattern", type=str, help="regex pattern")
    parser.add_argument('infile', nargs='*', type=argparse.FileType(mode='r', encoding='ascii'),
                        default=[sys.stdin], help="input files to search in")
    # parser.add_argument("files", nargs='+', type=str, help="path of desired files")
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

def print_matches(filehandlers, regex):
    for filehandler in filehandlers:
        line = filehandler.readline().strip()
        line_number = 0
        while line:
            line_number += 1
            for match in re.finditer(regex, line):
                print(f"{filehandler.name} {line_number} {line}")
            line = filehandler.readline().strip()


def print_underscore(filehandlers, regex):
    for filehandler in filehandlers:
        line = filehandler.readline().strip()
        line_number = 0
        while line:
            line_number += 1
            for match in re.finditer(regex, line):
                print(f"{filehandler.name} {line_number} {line}")
                amount_of_spaces = calc_underscore_start_position(filehandler.name, line_number, match.start())
                print(' ' * amount_of_spaces + "^")
            line = filehandler.readline().strip()


def calc_underscore_start_position(filename, line_number, match_start_position):
    return len(filename) + 1 + len(str(line_number)) + 1 + match_start_position


def print_colored(filehandlers, regex):
    for filehandler in filehandlers:
        line = filehandler.readline().strip()
        line_number = 0
        while line:
            line_number += 1
            for match in re.finditer(regex, line):
                print(f"{filehandler.name} {line_number}", end=" ")
                print(line[:match.start()] + '\033[0;36m' + match.group() + '\033[0;00m' + line[match.end():])
            line = filehandler.readline().strip()



def print_machine_format(filehandlers, regex):
    for filehandler in filehandlers:
        line = filehandler.readline().strip()
        line_number = 0
        while line:
            line_number += 1
            for match in re.finditer(regex, line):
                print(f"{filehandler.name}:{line_number}:{match.start()}:{match.group()}")
            line = filehandler.readline().strip()


def main():
    args = get_arguments()
    if args.underscore:
        print("underscore")
        print_underscore(args.infile, args.regex_pattern)
    elif args.color:
        print_colored(args.infile, args.regex_pattern)
    elif args.machine:
        print_machine_format(args.infile, args.regex_pattern)
    else:
        print_matches(args.infile, args.regex_pattern)


if __name__ == "__main__":
    main()
