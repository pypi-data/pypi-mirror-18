#!/usr/bin/env python

from __future__ import unicode_literals

import os
import subprocess
import unittest


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CLI = os.path.join(BASE_PATH, os.pardir, 'misspellings')


class Tests(unittest.TestCase):

    """Test the CLI.

    USAGE: misspellings [-f file] [files]
    Checks files for common spelling mistakes.
      -f file: File containing list of files to check.
      -m file: File containing list of misspelled words & corrections.
      -d     : Dump the list of misspelled words.
      -s file: Create a shell script to interactively correct the file.
      files: Zero or more files to check.

    """

    def test_good_file(self):
        p = subprocess.Popen([CLI, 'nine_mispellings.c'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (output, error_output) = p.communicate()
        self.assertEqual(error_output.decode(), '')
        self.assertEqual(len(output.decode().split('\n')), 10)
        self.assertEqual(p.returncode, 2)

    def test_bad_file(self):
        p = subprocess.Popen([CLI, 'missing.c'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (output, error_output) = p.communicate()
        self.assertEqual(output.decode(), '')
        self.assertEqual(len(error_output.decode().split('\n')), 2)
        self.assertEqual(p.returncode, 0)

    def test_good_flag_f(self):
        p = subprocess.Popen([CLI, '-f', 'good_file_list'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (output, error_output) = p.communicate()
        self.assertEqual(error_output.decode(), '')
        self.assertEqual(len(output.decode().split('\n')), 10)
        self.assertEqual(p.returncode, 2)

    def test_bad_flag_f(self):
        p = subprocess.Popen([CLI, '-f', 'broken_file_list'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (output, error_output) = p.communicate()
        self.assertEqual(output.decode(), '')
        self.assertEqual(len(error_output.decode().split('\n')), 2)
        self.assertEqual(p.returncode, 0)

    def test_bad_flag_m(self):
        p = subprocess.Popen([CLI, '-d', '-m', 'broken_msl.txt'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (output, error_output) = p.communicate()
        self.assertIn('ValueError', error_output.decode())
        self.assertEqual(output.decode(), '')
        self.assertEqual(p.returncode, 1)

    def test_good_flag_m(self):
        p = subprocess.Popen([CLI, '-d', '-m', 'small_msl.txt'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (output, error_output) = p.communicate()
        self.assertEqual(error_output.decode(), '')
        self.assertEqual(len(output.decode().split('\n')), 3)
        self.assertEqual(p.returncode, 0)

    def test_bad_flag_s(self):
        p = subprocess.Popen([CLI, '-s', 'various_spellings.c'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        (output, error_output) = p.communicate()
        self.assertIn('must not exist', error_output.decode())
        self.assertEqual(output.decode(), '')
        self.assertEqual(p.returncode, 2)

    def test_good_flag_s(self):
        test_out = os.path.join(BASE_PATH, 'various_spellings.test_out')
        good_out = os.path.join(BASE_PATH, 'various_spellings.good_out')
        if os.path.exists(test_out):
            os.unlink(test_out)
        p = subprocess.Popen([CLI, '-s', test_out,
                              'various_spellings.c'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        (output, error_output) = p.communicate(
            input='\n'.encode('utf8'))
        self.assertEqual(error_output.decode(), '')
        self.assertIn('withdrawl', output.decode())
        self.assertEqual(p.returncode, 0)

        with open(good_out, 'r') as good_file:
            good_contents = good_file.readlines()
        with open(test_out, 'r') as test_file:
            test_contents = test_file.readlines()
        self.assertListEqual(test_contents, good_contents)

    def test_standard_in(self):
        p = subprocess.Popen([CLI, '-f', '-'],
                             cwd=BASE_PATH,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        (output, error_output) = p.communicate(
            input='nine_mispellings.c\n'.encode('utf8'))
        self.assertEqual(error_output.decode(), '')
        self.assertEqual(len(output.decode().split('\n')), 10)
        self.assertEqual(p.returncode, 2)

if __name__ == '__main__':
    unittest.main()
