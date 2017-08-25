"""
    **************************************************************************
    |                                                                        |
    |                 TestVectorDirectoryParserApp.py 1.0                    |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Parses a directory for files of the specified type, outputs a simple   |
    | summary file. This code runs on python 2.4 or later.                   |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@postgrad.manchester.ac.uk                          |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | --dir (string) path to the directory to parse.                         |
    |                                                                        |
    | --out (string) path to the output file to create or append to.         |
    |                                                                        |
    | --ext (string) the file extension to look for during the parse.        |
    |                                                                        |
    | -f (int) the output format (1=CSV, 2=JSON).                            |
    |                                                                        |
    | -v the verbose logging flag.                                           |
    |                                                                        |
    **************************************************************************
    | License:                                                               |
    |                                                                        |
    | Code made available under the GPLv3 (GNU General Public License), that |
    | allows you to copy, modify and redistribute the code as you see fit    |
    | (http://www.gnu.org/copyleft/gpl.html). Though a mention to the        |
    | original author using the citation above in derivative works, would be |
    | very much appreciated.                                                 |
    **************************************************************************

"""

# Command Line processing Imports:
from optparse import OptionParser

# For general purposes
import os, sys, datetime

# For common operations.
from TestVectorDirectoryParser import TestVectorDirectoryParser
from Common import Common


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class TestVectorDirectoryParserApp(object):
    """
    Parses a test vector containing directory and outputs a summary file.

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

        Examples
        --------
        >>> python TestVectorDirectoryParserApp.py -dir /data/asc_dir -out Files.txt

        """
        # ****************************************
        #         Execution information
        # ****************************************

        print(__doc__)

        # ****************************************
        #    Command line argument processing
        # ****************************************

        # Python 2.4 argument processing.
        parser = OptionParser()

        # REQUIRED ARGUMENTS
        parser.add_option("--dir", action="store", dest="dir", help='Path to the directory to parse (required).', default=None)
        parser.add_option("--out", action="store", dest="out", help='Path to the output file (required).',default=None)
        parser.add_option("--ext", action="store", dest="ext", help='File extension to look for (required).',default='.fil')
        parser.add_option("-f"   , type="int"    , dest="format", help='The file output format (optional).',default=1)
        parser.add_option("-v", action="store_true", dest="verbose", help='Verbose debugging flag (optional).',default=False)

        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        directory     = args.dir
        output_file   = args.out
        output_format = args.format
        verbose = args.verbose

        ############################################################
        #              Check user supplied parameters              #
        ############################################################

        # Check the directory is valid...
        if directory is None:
            print "No valid directory supplied, exiting."
            sys.exit()
        elif not Common.dir_exists(directory):
            print "No valid directory supplied, exiting."
            sys.exit()

        # Check the output file is valid...
        if output_file is None:
            print "No valid output file supplied, exiting."
            sys.exit()
        elif not Common.is_path_valid(output_file):
            print "No valid output file supplied, exiting."
            sys.exit()

        # Check the output file is valid...
        if args.ext is None:
            print "No valid file extension supplied, exiting."
            sys.exit()
        else:
            extension = [args.ext]

        if output_format < 1 or output_format > 2:
            print "You must supply a valid output format via the -f flag."
            print "1    -    CSV."
            print "2    -    JSON (not implemented yet)."

            sys.exit()

        ############################################################
        #               Start parsing the directory                #
        ############################################################

        print "\tSearching: ", directory

        # Used to measure feature generation time.
        start = datetime.datetime.now()

        parser = TestVectorDirectoryParser()
        parser.parse(directory, extension, output_file, output_format)

        # Finally get the time that the procedure finished.
        end = datetime.datetime.now()

        ############################################################
        #                    Summarise outcome                     #
        ############################################################

        print "\tFinished parsing"
        print "\tExecution time: ", str(end - start)
        print "Done."

    # ****************************************************************************************************

if __name__ == '__main__':
    TestVectorDirectoryParserApp().main()
