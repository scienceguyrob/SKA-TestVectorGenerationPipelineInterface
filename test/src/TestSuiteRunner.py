"""
**************************************************************************
                                                                    
 TestSuite.py
                                                                    
**************************************************************************
 Description:                                                       
                                                                    
 Suite that executes all tests for the CandidateStreamer application.

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

# Used for logging purposes, please don't delete.
import logging
import sys
from unittest import TestLoader, TextTestRunner, TestSuite

from test.src.utilities.TestCommon import TestCommon


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class TestSuiteRunner(TestSuite):
    """                
    Executes unit tests on all scripts in the project.
    """

    def __init__(self):
        """
        Default constructor for the base class.

        Parameters
        ----------

        Returns
        ----------

        Examples
        --------
        >>>

        :return: N/A
        """

        # Create a logger object.
        super(TestSuiteRunner, self).__init__()
        self.logger = logging.getLogger('TestsSuite')

        # create a file handler
        handler = logging.FileHandler('TestsSuite.log')

        # Set the logging level.
        self.logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)

        # Create the logging format
        formatter = logging.Formatter('%(levelname)s,%(asctime)s,%(message)s', datefmt='%H:%M:%S')

        # Configure the logging handler with the desired output format
        handler.setFormatter(formatter)

        # Setup the log file writer
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(handler)
        self.logger.addHandler(ch)

    # ******************************
    #
    # MAIN METHOD AND ENTRY POINT.
    #
    # ******************************

    def main(self):
        """
        Main entry point for the Application.

        Parameters
        ----------

        Returns
        ----------

        Examples
        --------
        >>>
        """

        self.run_tests()

    # ****************************************************************************************************

    def run_tests(self):
        """
        Runs the tests in the test suite.

        Parameters
        ----------

        Returns
        ----------

        Examples
        --------
        >>>

        :return: N/A
        """

        self.logger.info('Running Unit Tests')

        loader = TestLoader()
        suite = TestSuite((
            loader.loadTestsFromTestCase(TestCommon)
        ))

        runner = TextTestRunner(verbosity=3)
        runner.run(suite)

        # ****************************************************************************************************


if __name__ == '__main__':
    TestSuiteRunner().main()
