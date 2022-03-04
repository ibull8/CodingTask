import pytest

import practice
import subprocess

#sanity: input: regex. 1 filename, output: one matched line
def test_one():
    regex="away"
    filename = "CodingTask/file1.txt"
    command = f"python3 practice.py {regex} {filename}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    err = result.stderr.decode('ascii')
    assert out == 'file1.txt 1 one line goes away goes\nfile1.txt 3 and I like to go away\n'

    assert err == ''

#multiple files via command line

#multiple matches per line


#input file via stdin


#matches are not overlapped

#no arguments given

#given file not exist


#optional arguments are mutually exclusive

#machine argument functionality

#color argument functionality

#underscore argument functionality

