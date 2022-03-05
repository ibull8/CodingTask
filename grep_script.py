import re
import argparse
import sys


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("regex_pattern", type=str, help="regex pattern")
    parser.add_argument('infile', nargs='*', type=argparse.FileType(mode='r'),
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


def get_print_function(args):
    if args.underscore:
        return print_underscore
    elif args.color:
        return print_colored
    elif args.machine:
        return print_machine_format
    else:
        return print_matches


def find_match(args):
    filehandlers = args.infile
    regex = args.regex_pattern

    for filehandler in filehandlers:
        line = filehandler.readline().strip()
        line_number = 0
        while line:
            line_number += 1
            for match in re.finditer(regex, line):
                # get_print_function returns the relevant print function to execute
                # and afterwards the print function is invoked
                get_print_function(args)(filehandler.name, line_number, match)
            line = filehandler.readline().strip()


def print_matches(filename, line_number, match):
    print("{filename} {line_number} {line}".format(filename=filename, line_number=line_number,
                                                   line=match.string))


def print_underscore(filename, line_number, match):
    print("{filename} {line_number} {line}".format(filename=filename, line_number=line_number,
                                                   line=match.string))
    amount_of_spaces = calc_underscore_start_position(filename, line_number, match.start())
    print(' ' * amount_of_spaces + "^")


def calc_underscore_start_position(filename, line_number, match_start_position):
    return len(filename) + 1 + len(str(line_number)) + 1 + match_start_position


def print_colored(filename, line_number, match):
    line = match.string
    print("{filename} {line_number} ".format(filename=filename, line_number=line_number) + line[:match.start()] +
          '\033[0;36m' + match.group() + '\033[0;00m' + line[match.end():])


def print_machine_format(filename, line_number, match):
    print("{filename}:{line_number}:{start_position}:{match}".format(filename=filename, line_number=line_number,
                                                                     start_position=match.start(), match=match.group()))


def main():
    args = get_arguments()
    find_match(args)


if __name__ == "__main__":
    main()
