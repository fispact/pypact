import unittest
import os
from pypact.util.file import *


class FileUnitTest(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../reference')
        self.filename_test91out = os.path.join(self.base_dir, "test91.out")
        self.filename_test91json = os.path.join(self.base_dir, "test91.json")
        self.filename_nofile = os.path.join(self.base_dir, "thisfilecannotpossiblyexist.out")

    def test_file_exists(self):
        self.assertEqual(file_exists(self.filename_test91out), True)
        self.assertEqual(file_exists(self.filename_test91json), True)
        self.assertEqual(file_exists(self.filename_nofile), False)
        self.assertEqual(file_exists(''), False)
        self.assertEqual(file_exists('thisfilecannotpossiblyexist.out'), False)

    def test_str_in_file(self):
        self.assertEqual(str_in_file(self.filename_test91out, "INITIAL CROSS SECTION DATA"), True)
        self.assertEqual(str_in_file(self.filename_test91out, "\n\n\n"), True)
        self.assertEqual(str_in_file(self.filename_test91out, "NUCLIDE        ATOMS"), True)
        self.assertEqual(str_in_file(self.filename_test91out, "NUCLIDE        ATOMS "), True)
        self.assertEqual(str_in_file(self.filename_test91out, " "), True)
        self.assertEqual(str_in_file(self.filename_test91out, "NUCLIDE        ATOMS x"), False)

    def test_content_as_str(self):
        self.assertTrue(content_as_str(self.filename_test91out) != [])
        self.assertEqual(
            len(content_as_str(self.filename_test91out)), nr_of_lines(self.filename_test91out, False), True)
        self.assertTrue(
            len(content_as_str(self.filename_test91out)) > nr_of_lines(self.filename_test91out, True))
        self.assertEqual(content_as_str(self.filename_test91out)[4].strip(),
                         '==============================================================================')

    def test_get_filename_no_ext(self):
        self.assertEqual(get_filename_ext(self.filename_test91out), '.out')
        self.assertEqual(get_filename_ext(self.filename_test91json), '.json')
        self.assertEqual(get_filename_ext(self.filename_nofile), '.out')
