from subprocess import Popen, PIPE

interpreter = "python2"
test_file_objective = "grep_script.py"


def run_test(command, expected_out, expected_error, stdin_text=None):
    proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if stdin_text:
        proc.stdin.write(stdin_text)
        out, err = proc.communicate()
        proc.stdin.close()
    else:
        out, err = proc.communicate()
    out, err = out.decode('ascii'), err.decode('ascii')
    print([out])
    print([err])
    assert out == expected_out
    assert err == expected_error


# one_file_and_one_match
def test_one_file_one_match():
    command = [interpreter, test_file_objective, "COPYRIGHT", "file1.txt"]
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n'
    expected_err = ''
    run_test(command, expected_out, expected_err)


# multiple matches per file
def test_one_file_multiple_matches():
    command = [interpreter, test_file_objective, "ELECTRONIC", "file1.txt"]
    expected_out = 'file1.txt 1 <<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAM\n' + \
                   'file1.txt 4 WITH PERMISSION.  ELECTRONIC AND MACHINE READABLE COPIES MAY BE\n'
    expected_err = ''
    run_test(command, expected_out, expected_err)


# input from multiple files
def test_matches_from_multiple_files():
    command = [interpreter, test_file_objective, "COPYRIGHT", "file1.txt", "file2.txt"]
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   'file2.txt 2 one owns a United States COPYRIGHT in these works, so the Foundation\n' + \
                   'file2.txt 4 permission and without paying COPYRIGHT royalties.  Special rules,\n'
    expected_err = ''
    run_test(command, expected_out, expected_err)


# multiple matches per line
def test_multiple_matches_on_one_line():
    command = [interpreter, test_file_objective, "[0-9]{4}", "file1.txt"]
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n'
    expected_err = ''
    run_test(command, expected_out, expected_err)


# input file via stdin
def test_input_via_standard_input():
    command = [interpreter, test_file_objective, "COPYRIGHT"]
    expected_out = '<stdin> 1 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n'
    expected_err = ''
    run_test(command, expected_out, expected_err,
             stdin_text="SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n")


# matches are not overlapped
def test_matches_not_overlapping():
    command = [interpreter, test_file_objective, "ABA", "file1.txt"]
    expected_out = 'file1.txt 9 ABABA\n'
    expected_err = ''
    run_test(command, expected_out, expected_err)


# no arguments given
def test_no_arguments_given():
    command = [interpreter, test_file_objective]
    expected_out = ''
    expected_err = 'usage: ' + test_file_objective + \
                   ' [-h] [-u | -c | -m] regex_pattern [infile [infile ...]]\n' + test_file_objective + ': error: ' + \
                   'too few arguments\n'
    run_test(command, expected_out, expected_err)


# given file not exist
def test_file_not_exist():
    command = [interpreter, test_file_objective, "[0-9]", "filetest"]
    expected_out = ''
    expected_err = "usage: " + test_file_objective + " [-h] [-u | -c | -m] regex_pattern [infile [infile ...]]\n" + \
                   test_file_objective + ": error: argument infile: can't open 'filetest': " + \
                   "[Errno 2] No such file or directory: 'filetest'\n"
    run_test(command, expected_out, expected_err)


# optional arguments are mutually exclusive
def test_arguments_mutually_exclusive():
    command = [interpreter, test_file_objective, "[0-9]", "file1.txt", "-c", "-u"]
    expected_out = ''
    expected_err = "usage: " + test_file_objective + " [-h] [-u | -c | -m] regex_pattern [infile [infile ...]]\n" + \
                   test_file_objective + ": error: argument -u/--underscore: not allowed with argument -c/--color\n"
    run_test(command, expected_out, expected_err)


# machine argument functionality
def test_machine_argument():
    command = [interpreter, test_file_objective, "[0-9]+", "file1.txt", "-m"]
    expected_out = 'file1.txt:2:25:1909\nfile1.txt:2:30:1993\nfile1.txt:5:36:1\nfile1.txt:6:24:2\n'
    expected_err = ''
    run_test(command, expected_out, expected_err)


# color argument functionality
def test_color_argument():
    command = [interpreter, test_file_objective, "19[0-9]{2}", "file1.txt", "-c"]

    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT \x1b[0;36m1909\x1b' + \
                   '[0;00m-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-\x1b[0;36m1993\x1b[0;00m BY WORLD LIBRARY, INC., AND IS\n'

    expected_err = ''
    run_test(command, expected_out, expected_err)


# underscore argument functionality
def test_underscore_argument():

    command = [interpreter, test_file_objective, "COPYRIGHT", "file1.txt", "-u"]
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   '                           ^\n'
    expected_err = ''
    run_test(command, expected_out, expected_err)


# no_match
def test_no_match():
    regex = "RedHat"
    filename = "tmp/file1.txt"
    command = [interpreter, test_file_objective, "RedHat", "file1.txt"]
    expected_out = ''
    expected_err = ''
    run_test(command, expected_out, expected_err)

