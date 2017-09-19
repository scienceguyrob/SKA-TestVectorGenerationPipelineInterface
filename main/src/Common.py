"""
**************************************************************************

 Common.py

**************************************************************************
 Description:

 Provides utility operations useful for reading data from files.

**************************************************************************
 Author: Rob Lyon
 Email : robert.lyon@manchester.ac.uk
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
import platform
import re


# ******************************
#
# CLASS DEFINITION
#
# ******************************


class Common(object):
    """
    Class that provides data manipulation methods.
    """

    @staticmethod
    def is_windows():
        """
        Tests if the application is running on a Windows OS.

        Parameters
        ----------
        :param: N/A

        Returns
        ----------
        :return: True if the application is running on a Windows OS, else false.

        """
        os_name = platform.system()

        if'Win' in os_name:
            return True
        else:
            return False

    # ****************************************************************************************************

    @staticmethod
    def is_mac():
        """
        Tests if the application is running on a MAC OS.

        Parameters
        ----------
        :param: N/A

        Returns
        ----------
        :return: True if the application is running on a MAC OS, else false.
        """
        os_name = platform.system()

        if 'Darwin' in os_name:
            return True
        else:
            return False

    # ****************************************************************************************************

    @staticmethod
    def is_unix():
        """
        Tests if the application is running on a Unix OS.

        Parameters
        ----------
        :param: N/A

        Returns
        ----------
        :return: True if the application is running on a Unix OS, else false.
        """
        os_name = platform.system()

        if 'nux' in os_name:
            return True
        else:
            return False

    # ****************************************************************************************************

    @staticmethod
    def is_valid_unix_path(path):
        """
        Checks if a string is a valid unix path.

        Parameters
        ----------
        :param path: the path to check for validity.

        Returns
        ----------
        :return: true if the path is valid for unix systems, else false.

        """

        if str(path) == "":
            return False

        regex = '((?:\\/[\\w\\.\\-]+)+)'
        rg = re.compile(regex, re.IGNORECASE | re.DOTALL)
        m = rg.search(path)

        if m:
            return True
        else:
            if os.path.isfile(path):
                return True
            elif not os.path.isfile(path):
                open(path, 'a')

                if os.path.isfile(path):
                    os.remove(path)
                    return True
                else:
                    return False
            else:
                return False

    # ****************************************************************************************************

    @staticmethod
    def is_valid_windows_path(path):
        """
        Checks if a string is a valid windows path.

        Parameters
        ----------
        :param path: the path to check for validity.

        Returns
        ----------
        :return: true if the path is valid for windows systems, else false.
        """
        if path is None:
            return False
        elif len(path) == 3:  # e.g. C:\
            return
        elif str(path).endswith("\\"):
            return False
        else:

            # Invalid path characters to explicitly check for .
            invalid_chars = ["\"", "/", "*", "?", "<", ">", "|"]

            for c in invalid_chars:
                if c in str(path):
                    return False

            regex = '"([a-z]:\\\\(?:[-\\w\\.\\d]+\\\\)*(?:[-\\w\\.\\d]+)?)"'
            rg = re.compile(regex, re.IGNORECASE | re.DOTALL)
            m = rg.search(path)

            if m:
                return True
            else:
                return False

    # ****************************************************************************************************

    @staticmethod
    def is_path_valid(pth):
        """
        Checks if a string is a valid path for the operating system the application
        is running upon.

        Parameters
        ----------
        :param pth: the path to check for validity.

        Returns
        ----------
        :return: true if the path is valid, else false.
        """

        if pth is None:
            return False

        # Check for relative path
        if os.path.isabs(pth):
            path = pth
        else:
            path = os.path.abspath(pth)

        try:
            if Common.is_windows():
                return Common.is_valid_windows_path(path)
            elif Common.is_mac():
                return Common.is_valid_unix_path(path)
            elif Common.is_unix():
                return Common.is_valid_unix_path(path)
            else:
                return True
        except IOError:
            return False

    # ****************************************************************************************************

    @staticmethod
    def read_file(path):
        """
        Reads in a file, returns the data as a list. If the file does
        not exist, a None object is returned. If the file contains no
        data, a None object is also returned.

        Parameters
        ----------
        :param path: the full path to the file to read.

        Returns
        ----------
        :return: the lines of the file stored as a list, else a None object if the file is empty or non-existent.

        """

        if not Common.is_path_valid(path):
            return None

        if Common.file_exists(path):

            f = open(path)
            contents = f.readlines()
            f.close()

            if contents is None:
                return None
            elif len(contents) == 0:
                return None
            else:
                return contents

        else:
            return None

    # ****************************************************************************************************

    @staticmethod
    def read_file_as_string(path):
        """
        Reads in a file, returns the data as a string. If the file does
        not exist, a None object is returned. If the file contains no
        data, a None object is also returned.

        Parameters
        ----------
        :param path: the full path to the file to read.

        Returns
        ----------
        :return: the lines of the file stored as a string, else a None object if the file is empty or non-existent.

        """

        if not Common.is_path_valid(path):
            return None

        if Common.file_exists(path):

            f = open(path)
            contents = f.read()
            f.close()

            if contents is None:
                return None
            elif len(contents) == 0:
                return None
            else:
                return contents
        else:
            return None

    # ****************************************************************************************************

    @staticmethod
    def append_to_file(path, text):
        """
        Appends the provided text to the file at the specified path.

        Parameters
        ----------
        :param path: the path to the file to append text to.
        :param text: the text to append to the file.

        Returns
        ----------
        N/A (python can't check if file was written to!).
        Examples
        --------
        >>>

        Parameters:
        path    -    the path to the file to append text to.
        text    -    the text to append to the file.

        """

        output_file = open(path, 'a')
        output_file.write(str(text))
        output_file.close()

    # ****************************************************************************************************

    @staticmethod
    def dir_exists(pth):
        """
        Checks a directory exists, returns true if it does, else false.

        Parameters
        ----------
        :param pth: the path to the directory.

        Returns
        ----------
        True if the directory exists, else false.

        """

        # Check for relative path
        if os.path.isabs(pth):
            path = pth
        else:
            path = os.path.abspath(pth)

        if os.path.isdir(path):
            return True

        if not Common.is_path_valid(path):
            return False

        try:
            if os.path.isdir(path):
                return True
            else:
                return False
        except IOError:
            return False

    # ****************************************************************************************************

    @staticmethod
    def file_exists(path):
        """
        Checks a file exists, returns true if it does, else false.

        Parameters
        ----------
        :param path: the path to the file.

        Returns
        ----------
        :return: True if the file exists, else false.

        """
        if not Common.is_path_valid(path):
            return False

        try:
            if os.path.isfile(path):
                return True
            else:
                return False
        except IOError:
            return False

    # ****************************************************************************************************

    @staticmethod
    def get_file_name(path):
        """
        Extracts the file name from the supplied path.

        Parameters
        ----------
        :param path: the path to the file.

        Returns
        ----------
        :return: the file name as a string with its full extension, else None if an error is encountered.

        """

        # First check the path is valid.
        if Common.is_path_valid(path):

            head, tail = os.path.split(path)

            # Check if string is not equal to '' i.e. empty.
            if tail:
                return str(tail)
            else:
                return None
        else:
            return None

    # ****************************************************************************************************

    @staticmethod
    def delete_file(path):
        """
        Deletes the file at the supplied path.

        Parameters
        ----------
        :param path: the path to the file.

        Returns
        ----------
        :return: true if the file was deleted or does not exist, else false.
        """

        # First check the path is valid.
        if Common.is_path_valid(path):

            if Common.file_exists(path):
                os.remove(path)

                if Common.file_exists(path):
                    return False
                else:
                    return True
            else:
                return False
        else:
            return True

    # ****************************************************************************************************

    @staticmethod
    def create_file(path):
        """
        Creates the file at the supplied path.

        Parameters
        ----------
        :param path: the path to the file.

        Returns
        ----------
        :return: true if the file was created or already exists, else false.
        """
        # First check the path is valid.
        if Common.is_path_valid(path):

            if not os.path.isfile(path):
                open(path, 'a')

                if Common.file_exists(path):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    # ****************************************************************************************************

    @staticmethod
    def create_dir(path):
        """
        Creates the directory at the supplied path.

        Parameters
        ----------
        :param path: the path to the directory.

        Returns
        ----------
        :return: true if the directory was created or already exists, else false.
        """
        # First check the path is valid.
        if Common.is_path_valid(path):

            if not os.path.isdir(path):
                os.makedirs(path)

                if Common.dir_exists(path):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    # ****************************************************************************************************

    @staticmethod
    def delete_dir(path):
        """
        Deletes the directory at the supplied path.

        Parameters
        ----------
        :param path: the path to the file.

        Returns
        ----------
        :return: true if the directory was deleted or does not exist, else false.
        """

        # First check the path is valid.
        if Common.is_path_valid(path):

            if Common.dir_exists(path):
                os.removedirs(path)

                if Common.dir_exists(path):
                    return False
                else:
                    return True
            else:
                return False
        else:
            return True

    # ****************************************************************************************************

    @staticmethod
    def file_size_bits(path):
        """
        Gets the size of a file in bits.

        Parameters
        ----------
        :param path: the path to the file.

        Returns
        ----------
        :return: the size of the file in bits, else 0 if the file does not exist.
        """
        if not Common.is_path_valid(path):
            return 0

        try:
            if os.path.isfile(path):
                return os.path.getsize(path) * 8
            else:
                return 0
        except IOError:
            return 0

    # ****************************************************************************************************
