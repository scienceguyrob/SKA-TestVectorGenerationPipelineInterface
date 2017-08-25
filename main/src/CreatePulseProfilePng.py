"""
    **************************************************************************
    |                                                                        |
    |                 CreatePulsarProfilePng.py 1.0                          |
    |                                                                        |
    **************************************************************************
    | Description:                                                           |
    |                                                                        |
    | Parses a directory for files of the specified type (.asc), and outputs |
    | a PNG for each valid file found. This code runs on python 2.4 or later.|
    **************************************************************************
    | Author: Rob Lyon                                                       |
    | Email : robert.lyon@postgrad.manchester.ac.uk                          |
    | web   : www.scienceguyrob.com                                          |
    **************************************************************************
    | Required Command Line Arguments:                                       |
    |                                                                        |
    | --dir (string) path to the directory containing .asc files.            |
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
import os
import sys
import datetime

# For common operations.
from Common import Common

import matplotlib.pyplot as plt

# ******************************
#
# CLASS DEFINITION
#
# ******************************


class CreatePulsarProfilePng(object):
    """
    Parses a directory containing .asc files, and produces PNG plots
    of the pulse. The plots are created using Matplotlib.

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

        (args, options) = parser.parse_args()

        # Update variables with command line parameters.
        directory = args.dir

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

        ############################################################
        #               Start parsing the directory                #
        ############################################################

        print "\tSearching: ", directory

        # Count of the profile files found.
        ascFileCount = 0

        # Used to measure processing time.
        start = datetime.datetime.now()

        # For each type of file this program recognises...
        for filetype in ['.asc']:

            # Loop through the specified directory
            for root, subFolders, filenames in os.walk(directory):

                # If the file type matches '.asc'

                for file_name in filenames:

                    # Double check it is a .asc file
                    if file_name.endswith(filetype):

                        # Increment asc file count,  as we have found
                        # a valid file.
                        ascFileCount += 1

                        # Get the full path to the file.
                        full_file_path = os.path.join(root, file_name)

                        # Read the data in from the .asc file. This data
                        # should describe a valid pulse profile. The file
                        # should be structured so that there is only a single
                        # data item on each line, e.g.,
                        #
                        # 0.4
                        # 0.5
                        # 0.3
                        # 0.9
                        # ...
                        #
                        # So each line should be read, and the data extracted.
                        data_str = Common.read_file(full_file_path)

                        if data_str is None:
                            print 'File empty: ', file_name
                        else:

                            data_points = len(data_str)

                            # Check there is more than 1 data point
                            if data_points < 1:
                                print 'Too few data points in file: ', file_name
                            else:
                                # Now store the data in a simple list.
                                data = []

                                try:
                                    # For each data item, try to cast as a float
                                    # if the cast files, the file is invalid. The
                                    # file should contain only numerical values.
                                    for s in data_str:
                                        d = float(s)
                                        data.append(d)

                                except Exception as e:
                                    print 'Error converting numerical values to float in file: ', file_name
                                    print 'Does the file contain strings or invalid characters? '

                                # If the code above succeeded, there should be more than
                                # 1 data item in the list.
                                if len(data) > 0:

                                    # From the .asc file name, we can get the pulsar name.
                                    # The asc file should be named as follows:
                                    #
                                    # <Pulsar>_<Freq>_<version>.asc
                                    #
                                    # Where the version element may or may not be included.

                                    # So for example file names could include,
                                    #
                                    # J0000+0000_1400.asc
                                    # J0000-0000_1400.asc
                                    # J0000+0000_1400_1.asc
                                    # J0000-0000_1400_1.asc
                                    # J0000+0000_1400_2.asc
                                    # J0000-0000_1400_2.asc
                                    # J0000+0000_600.asc
                                    # J0000-0000_600.asc
                                    # ...
                                    #
                                    # etc.
                                    file_name_components = file_name.replace('.asc', '').split('_')

                                    if file_name_components is None:
                                        print 'Unexpected .asc file name - must be of form <Pulsar>_<Freq>.asc'
                                    else:

                                        if len(file_name_components) <= 1:
                                            print 'Unexpected .asc file name - must be of form <Pulsar>_<Freq>.asc'
                                        else:

                                            # Get pulsar name and frequency
                                            name = str(file_name_components[0])
                                            freq = str(file_name_components[1])

                                            # Now produce the plot
                                            fig = plt.figure(figsize=(3, 3))
                                            ax = plt.subplot(111)
                                            ax.plot(data)
                                            ax.set_xlim([0, data_points])
                                            ax.set_ylabel('Intensity')
                                            ax.set_xlabel('Bin')

                                            # Remove axis ticks
                                            ax.set_yticklabels([])
                                            ax.set_xticklabels([])
                                            plt.axis('off')

                                            title = name + ' @: ' + freq + ' MHz'
                                            plt.title(title)

                                            # Now save the image file. If the destination file
                                            # path exists, simply delete it, then create the
                                            # new image.
                                            if Common.file_exists(full_file_path.replace('.asc', '.png')):
                                                Common.delete_file(full_file_path.replace('.asc', '.png'))

                                            fig.savefig(full_file_path.replace('.asc', '.png'))

                                            # Must close to prevent memory issues.
                                            plt.close(fig)

        # Finally get the time that the procedure finished.
        end = datetime.datetime.now()

        ############################################################
        #                    Summarise outcome                     #
        ############################################################

        print "\tFinished parsing"
        print "\tTotal .asc files found: ", str(ascFileCount)
        print "\tExecution time: ", str(end - start)
        print "Done."

    # ****************************************************************************************************

if __name__ == '__main__':
    CreatePulsarProfilePng().main()
