"""
**************************************************************************

 TestHashComputeTimes.py

**************************************************************************
 Description:

Tests how long it takes to do an MD5 hash, on files of various sizes.

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

# For general purposes
import os, hashlib, datetime


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class TestHashComputeTimes(object):
    """
    Runs the test

    """

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    def main(self, args=None):
        """
        Main entry point for the Application.

        Parameters
        ----------
        :param args: command line arguments.

        Returns
        ----------
        :return: N/A

        """

        ############################################################
        #              Start creating the large file               #
        ############################################################

        One_GB = 1024 * 1024 * 1024 *4  # 1GB
        with open('large_file.txt', 'wb') as fout:
            fout.write(os.urandom(One_GB))

        ############################################################
        #               Start computing the hash                   #
        ############################################################

        # Used to measure feature generation time.
        start = datetime.datetime.now()

        self.generate_file_md5('large_file.txt', 8192)

        # Finally get the time that the procedure finished.
        end = datetime.datetime.now()

        ############################################################
        #                    Summarise outcome                     #
        ############################################################

        print "\tFinished testing"
        print "\tExecution time: ", str(end - start)
        print "Done."
    # ****************************************************************************************************

    def generate_file_md5(self, path, blocksize=8192):
        """
        Computes the MD5 hash of the file at the specified path.
        ----------
        :param path: the full path to the file to compute the hash for.
        :param blocksize: determines how much data is read in from the file at a time.

        ----------
        :return: an MD5 hash of the file.
        """
        m = hashlib.md5()
        with open(path, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)

        return m.hexdigest()

    # ****************************************************************************************************

if __name__ == '__main__':
    TestHashComputeTimes().main()
