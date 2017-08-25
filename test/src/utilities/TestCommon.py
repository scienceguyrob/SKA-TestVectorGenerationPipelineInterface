"""
**************************************************************************

 TestCommon.py

**************************************************************************
 Description:

 Tests the common utility methods.

**************************************************************************
 Author: Rob Lyon
 Email : robert.lyon@postgrad.manchester.ac.uk
 web   : www.scienceguyrob.com

**************************************************************************
 Required Command Line Arguments:

 N/A

**************************************************************************
 Optional Command Line Arguments:

 N/A

**************************************************************************
 License:

 Code made available under the GPLv3 (GNU General Public License), that
 allows you to copy, modify and redistribute the code as you see fit
 (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
 original author using the citation above in derivative works, would be
 very much appreciated.

**************************************************************************
"""

import os
import unittest

from main.src.Common import Common


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class TestCommon(unittest.TestCase):
    """
    The tests for the Common class.
    """

    # Points to the resource directory containing test files.
    data_root = 'resources'
    test_data_root = data_root + '/'

    # Points to the resource directory containing test files.
    data_root = os.path.abspath('../..') + '/resources'
    test_data_root = data_root + '/test/'

    # Some test file paths.
    dir_a = test_data_root + 'A'
    file_b = test_data_root + 'B.txt'
    file_c = test_data_root + 'C.txt'
    file_d = test_data_root + 'D.txt'
    file_e = test_data_root + 'E'

    # ******************************
    #
    # TESTS
    #
    # ******************************

    def test_is_path_valid(self):
        """ Tests the methods that checks if a string is a system path."""

        # Tests are:
        #
        # Test when path is to existing file.
        # Test when path is valid, pointing to non-existent file or directory.
        # Test when path is invalid.

        self.assertTrue(Common.is_path_valid(self.dir_a))
        self.assertTrue(Common.is_path_valid(self.file_b))
        self.assertTrue(Common.is_path_valid(self.file_c))
        self.assertTrue(Common.is_path_valid(self.file_d))
        self.assertTrue(Common.is_path_valid(self.file_e))

        # Test when path is valid, pointing to non-existent file or directory.
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/X.txt" + os.pathsep + "A.txt"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/Y.txt" + os.pathsep + "A.zip"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/Z.txt" + os.pathsep + "A.a"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/X.txt" + os.pathsep + "b.txt"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/Y.txt" + os.pathsep + "a_b.txt"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/Z.txt" + os.pathsep + "a.txt"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/."))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "FAKE/%"))

        # Test when path is invalid.
        self.assertTrue(Common.is_path_valid(self.test_data_root + "?"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "\\"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + ":"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "*"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "|"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "\""))
        self.assertTrue(Common.is_path_valid(self.test_data_root + "<"))
        self.assertTrue(Common.is_path_valid(self.test_data_root + ">"))

    # ****************************************************************************************************

    def test_read_file(self):
        """ Tests the methods that reads a file into a list object."""

        self.assertIsNone(Common.read_file(''))
        self.assertIsNone(Common.read_file(None))
        self.assertIsNone(Common.read_file('fake/path/file.txt'))

        self.assertEqual(Common.read_file(self.file_b), ['1,2,3,4,5'])
        self.assertEqual(Common.read_file(self.file_c), ['1'])

    # ****************************************************************************************************

    def test_append_to_file(self):
        """ Tests the methods that appends text to a file."""

        # Create the file
        self.assertTrue(Common.create_file(self.test_data_root + 'Z.txt'))

        Common.append_to_file(self.test_data_root + 'Z.txt', '1,2,3,4,5')

        # Now check contents are as expected
        self.assertEqual(Common.read_file_as_string(self.test_data_root + 'Z.txt'), '1,2,3,4,5')

        # Delete the file
        self.assertTrue(Common.delete_file(self.test_data_root + 'Z.txt'))
        # Now check file was deleted
        self.assertFalse(Common.file_exists(self.test_data_root + 'Z.txt'))

    # ****************************************************************************************************

    def test_delete_file(self):
        """ Tests the method that deletes a file."""

        self.assertTrue(Common.delete_file(''))
        self.assertTrue(Common.delete_file(None))
        # Create the file
        self.assertTrue(Common.create_file(self.test_data_root + 'Z.txt'))
        # Delete the file
        self.assertTrue(Common.delete_file(self.test_data_root + 'Z.txt'))
        # Now check file was deleted
        self.assertFalse(Common.file_exists(self.test_data_root + 'Z.txt'))

    # ****************************************************************************************************

    def test_delete_dir(self):
        """ Tests the method that deletes a directory."""

        self.assertTrue(Common.delete_dir(''))
        self.assertTrue(Common.delete_dir(None))
        # Create the dir
        self.assertTrue(Common.create_dir(self.test_data_root + 'Z'))
        # Delete the dir
        self.assertTrue(Common.delete_dir(self.test_data_root + 'Z'))
        # Now check file was deleted
        self.assertFalse(Common.dir_exists(self.test_data_root + 'Z'))

    # ****************************************************************************************************

    def test_create_dir(self):
        """ Tests the method that creates a directory."""

        self.assertFalse(Common.create_dir(''))
        self.assertFalse(Common.create_dir(None))
        # Create the dir
        self.assertTrue(Common.create_dir(self.test_data_root + 'Z'))
        # Delete the dir
        self.assertTrue(Common.delete_dir(self.test_data_root + 'Z'))
        # Now check dir was deleted
        self.assertFalse(Common.dir_exists(self.test_data_root + 'Z'))

    # ****************************************************************************************************

    def test_create_file(self):
        """ Tests the method that creates a file."""

        self.assertFalse(Common.create_file(''))
        self.assertFalse(Common.create_file(None))
        # Create the file
        self.assertTrue(Common.create_file(self.test_data_root + 'Z.txt'))
        # Delete the file
        self.assertTrue(Common.delete_file(self.test_data_root + 'Z.txt'))
        # Now check file was deleted
        self.assertFalse(Common.file_exists(self.test_data_root + 'Z.txt'))

    # ****************************************************************************************************

    def test_dir_exists(self):
        """ Tests the methods that checks if a directory exists."""

        self.assertTrue(Common.dir_exists(self.dir_a))

        self.assertFalse(Common.dir_exists(None))
        self.assertFalse(Common.dir_exists(''))
        self.assertFalse(Common.dir_exists('/fake/dir'))

    # ****************************************************************************************************

    def test_file_exists(self):
        """ Tests the methods that checks if a file exists."""

        self.assertTrue(Common.file_exists(self.file_b))
        self.assertTrue(Common.file_exists(self.file_c))
        self.assertTrue(Common.file_exists(self.file_d))
        self.assertTrue(Common.file_exists(self.file_e))

        self.assertFalse(Common.file_exists(self.dir_a))
        self.assertFalse(Common.file_exists(self.test_data_root + "FAKE/X.txt" + os.pathsep + "A.txt"))
        self.assertFalse(Common.file_exists(self.test_data_root + "FAKE/Y.txt" + os.pathsep + "A.zip"))
        self.assertFalse(Common.file_exists(self.test_data_root + "FAKE/Z.txt" + os.pathsep + "A.a"))
        self.assertFalse(Common.file_exists(self.test_data_root + "FAKE/X.txt" + os.pathsep + "b.txt"))
        self.assertFalse(Common.file_exists(self.test_data_root + "FAKE/Y.txt" + os.pathsep + "a_b.txt"))
        self.assertFalse(Common.file_exists(self.test_data_root + "FAKE/Z.txt" + os.pathsep + "a.txt"))

    # ****************************************************************************************************

    def test_get_file_name(self):
        """ Tests the method that extracts a file's name from its full path."""

        # Should get none for these entries
        self.assertIsNone(Common.get_file_name(''))
        self.assertIsNone(Common.get_file_name(None))

        self.assertEquals(Common.get_file_name(self.dir_a), 'A')
        self.assertEquals(Common.get_file_name(self.file_b), 'B.txt')
        self.assertEquals(Common.get_file_name(self.file_c), 'C.txt')
        self.assertEquals(Common.get_file_name(self.file_d), 'D.txt')
        self.assertEquals(Common.get_file_name(self.file_e), 'E')

    # ****************************************************************************************************

    # ******************************
    #
    # Test Setup & Teardown
    #
    # ******************************

    # preparing to test
    def setUp(self):
        """ Setting up for the test """

    # ****************************************************************************************************

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    # ****************************************************************************************************

    if __name__ == "__main__":
        unittest.main()
