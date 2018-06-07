import unittest
import os
import mock

from tests.testerbase import REFERENCE_DIR

from pypact.util.file import *


class FileUnitTest(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.join(REFERENCE_DIR)
        self.filename_test91out = os.path.join(self.base_dir, "test91.out")
        self.filename_test91json = os.path.join(self.base_dir, "test91.json")
        self.filename_nofile = os.path.join(self.base_dir, "thisfilecannotpossiblyexist.out")

    @mock.patch('pypact.util.file.os.path')
    def test_file_exists_mock(self, mock_path):
        # file does not exist
        mock_path.isfile.return_value = False
        self.assertFalse(file_exists("any path"), "File is not present.")

        # make the file 'exist'
        mock_path.isfile.return_value = True
        self.assertTrue(file_exists("any path"), "File is present.")

    @mock.patch('pypact.util.file.os.path')
    def test_dir_exists_mock(self, mock_path):
        # dir does not exist
        mock_path.isdir.return_value = False
        self.assertFalse(dir_exists("any path"), "Directory is not present.")

        # make the file 'exist'
        mock_path.isdir.return_value = True
        self.assertTrue(dir_exists("any path"), "Directory is present.")
    
    @mock.patch('pypact.util.file.os')
    def test_file_remove_mock(self, mock_os):
        # file does not exist
        mock_os.path.isfile.return_value = False
        file_remove("any path")
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")

        # make the file 'exist'
        mock_os.path.isfile.return_value = True
        file_remove("any path")
        self.assertTrue(mock_os.remove.called, "Failed to remove the file when present.")
        mock_os.remove.assert_called_with("any path")
    
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
