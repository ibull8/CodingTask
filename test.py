import pytest

import practice
import subprocess


# one_file_and_one_match
def test_one_file_one_match():
    regex = "COPYRIGHT"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    assert out == 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n'
    assert err == ''


# multiple matches per file
def test_one_file_multiple_matches():
    regex = "ELECTRONIC"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    expected_out = 'file1.txt 1 <<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAM\n' + \
                   'file1.txt 4 WITH PERMISSION.  ELECTRONIC AND MACHINE READABLE COPIES MAY BE\n'
    assert out == expected_out
    assert err == ''


# input from multiple files
def test_matches_from_mutiple_files():
    regex = "COPYRIGHT"
    filename = "file1.txt file2.txt"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   'file2.txt 2 one owns a United States COPYRIGHT in these works, so the Foundation\n' + \
                   'file2.txt 4 permission and without paying COPYRIGHT royalties.  Special rules,\n'
    assert out == expected_out
    assert err == ''


# multiple matches per line
def test_multiple_matches_on_one_line():
    regex = "[0-9]{4}"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n'
    assert out == expected_out
    assert err == ''


# input file via stdin
def test_input_via_standard_input():
    regex = "COPYRIGHT"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} < {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    assert out == '<stdin> 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n'
    assert err == ''


# matches are not overlapped
def test_matches_not_overlapping():
    regex = "ABA"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    assert out == 'file1.txt 9 ABABA\n'
    assert err == ''


# no arguments given
def test_no_arguments_given():
    regex = ""
    filename = ""
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    print([err])
    expected_error = 'usage: practice.py [-h] [-u | -c | -m] regex_pattern [infile [infile ...]]\n' + \
                     'practice.py: error: the following arguments are required: regex_pattern\n'
    assert out == ''
    assert err == expected_error


# given file not exist
def test_file_not_exist():
    regex = "[0-9]"
    filename = "filetest"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    print([err])
    expected_error = "usage: practice.py [-h] [-u | -c | -m] regex_pattern [infile [infile ...]]\n" + \
                     "practice.py: error: argument infile: can't open 'filetest': " + \
                     "[Errno 2] No such file or directory: 'filetest'\n"
    assert out == ''
    assert err == expected_error


# optional arguments are mutually exclusive
def test_arguments_mutually_exclusive():
    regex = "[0-9]"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename} -c -u"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    print([err])
    expected_error = "usage: practice.py [-h] [-u | -c | -m] regex_pattern [infile [infile ...]]\n" + \
                     "practice.py: error: argument -u/--underscore: not allowed with argument -c/--color\n"
    assert out == ''
    assert err == expected_error


# machine argument functionality
def test_machine_argument():
    regex = "[0-9]+"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename} -m"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    print([out])
    print([err])
    assert out == 'file1.txt:2:25:1909\nfile1.txt:2:30:1993\nfile1.txt:5:36:1\nfile1.txt:6:24:2\n'
    assert err == ''


# color argument functionality
def test_color_argument():
    regex = "19[0-9]{2}"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename} -c"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT \x1b[0;36m1909\x1b' + \
                   '[0;00m-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-\x1b[0;36m1993\x1b[0;00m BY WORLD LIBRARY, INC., AND IS\n'
    assert out == expected_out
    assert err == ''


# underscore argument functionality
def test_underscore_argument():
    regex = "COPYRIGHT"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename} -u"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    expected_out = 'file1.txt 2 SHAKESPEARE IS COPYRIGHT 1909-1993 BY WORLD LIBRARY, INC., AND IS\n' + \
                   '                           ^\n'
    assert out == expected_out
    assert err == ''

# no_match
def test_no_match():
    regex = "RedHat"
    filename = "file1.txt"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    assert out == ''
    assert err == ''
