"""
    **************************************************************************
    |                                                                        |
    |                       PageBuilderApp.py 1.0                            |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Builds a simple webpage that describes and summarises SKA test vectors.|
    | This code runs on python 2.4 or later.                                 |
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@postgrad.manchester.ac.uk                          |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | --in (string) path to the test vector database input file to parse.    |
    |                                                                        |
    | --out (string) path to the output file to create or append to.         |
    |                                                                        |
    | -f (int) the output format (1=CSV, 2=JSON).                            |
    |                                                                        |
    | --asc (string) path to the directory containing .asc files.            |
    |                                                                        |
    | --batch (string) path to the directory containing text files describing|
    |                  test vector processing batches. Batch files should be |
    |                  named like Batch_<Batch number>.txt.                  |
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
import sys
import datetime

# For common operations.
from PageBuilder import PageBuilder
from Common import Common


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class PageBuilderApp(object):
    """
    Builds the HTML file.

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
        >>> python DirectoryParserApp.py -dir /data/asc_dir -out Files.txt

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
        parser.add_option("--in", action="store", dest="input", help='Path to the input file to parse (required).', default=None)
        parser.add_option("--out", action="store", dest="out", help='Path to the output file (required).',default=None)
        parser.add_option("--asc", action="store", dest="asc", help='Path to the .asc directory (required).', default=None)
        parser.add_option("--batch", action="store", dest="batch", help='Path to the batch directory (required).',default=None)
        parser.add_option("-f"   , type="int"    , dest="format", help='The file output format (optional).',default=1)

        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        input_file    = args.input
        output_file   = args.out
        output_format = args.format
        asc_dir       = args.asc
        batch_dir     = args.batch

        # Check the directory is valid...
        if asc_dir is None:
            print "No valid .asc directory supplied, exiting."
            sys.exit()
        elif not Common.dir_exists(asc_dir):
            print "No valid .asc directory supplied, exiting."
            sys.exit()

        # Check the directory is valid...
        if batch_dir is None:
            print "No valid batch directory supplied, exiting."
            sys.exit()
        elif not Common.dir_exists(batch_dir):
            print "No valid batch directory supplied, exiting."
            sys.exit()

        # Check the directory is valid...
        if input_file is None:
            print "No valid input file supplied, exiting."
            sys.exit()
        elif not Common.file_exists(input_file):
            print "No valid input file supplied, exiting."
            sys.exit()

        # Check the output file is valid...
        if output_file is None:
            print "No valid output file supplied, exiting."
            sys.exit()
        elif not Common.is_path_valid(output_file):
            print "No valid output file supplied, exiting."
            sys.exit()

        if output_format < 1 or output_format > 2:
            print "You must supply a valid output format via the -f flag."
            print "1    -    CSV."
            print "2    -    JSON (not implemented yet)."

            sys.exit()

        print "Processing: ", input_file

        # Used to measure run time.
        start = datetime.datetime.now()

        builder = PageBuilder()
        builder.build(input_file, output_file, output_format, asc_dir, batch_dir)

        # Finally get the time that the procedure finished.
        end = datetime.datetime.now()

        print "\tFinished building"
        print "\tExecution time: ", str(end - start)
        print "Done."

    # ****************************************************************************************************

if __name__ == '__main__':
    PageBuilderApp().main()
