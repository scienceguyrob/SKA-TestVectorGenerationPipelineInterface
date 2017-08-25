"""
**************************************************************************

 TestVectorDirectoryParser.py

**************************************************************************
 Description:

 Parses a directory containing SKA test vectors, and obtains their details.
 This is only to be used with directories containing SKA test vector filter-
 bank files. It expects these files to be in the following format:

 <Type>_<Batch>_<Period>_<DM>_<Z>_<S/N>_<EPN Pulsar Name>_<Freq MHz>.fil

 Where,

 Type            = the type of test vector, e.g., fake pulsar.
 Batch           = the batch the test vector was generated within.
 Period          = The period of the injected signal in the test vector (ms).
 DM              = The dispersion measure of the injected signal.
 Z               = The acceleration applied to the inserted signal.
 S/N             = The signal-to-noise (S/N of the injected signal.
 EPN Pulsar Name = The pulsar whose integrated pulse profile was used to
                    create the test vector (from the EPN database).
 Freq            = The frequency the pulsar from the EPN database (whose
                   profile was injected in to the test vector) was observed
                   at, in MHz.


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
import os
import datetime
import hashlib
import DataConversions

# For common operations
from Common import Common


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class TestVectorDirectoryParser(object):
    """
    Parses a directory containing one or more test vector files, of the specified
    file type. When a file is found, its details are recorded to a CSV or JSON
    string, and written to an output file.
    """

    # ****************************************************************************************************

    def parse(self, directory, fileExtensions, output_file, output_format):
        """
        Reads the target directory, and records the files found which
        have the specified file extension.

        Parameters
        ----------
        :param directory: the directory containing the files to be parsed.
        :param fileExtensions: a list containing the file extensions to look for.
        :param output_file: the output path to record information to.
        :param output_format: the output format, i.e. CSV or JSON.

        Returns
        ----------
        N/A

        """

        # ****************************************
        #    Look for test vector database file
        # ****************************************

        # Create dictionary which stores test vector entries,
        # if there are any...
        test_vectors = {}
        changed_vectors = {}

        if Common.file_exists(output_file):
            # We have an existing test vector database file.
            "\t\tAn existing test vector database file was found: ", output_file

            # We expect a CSV file of the following format:
            #
            #
            # <Filename>,<Batch>,<Type>,<Period (ms)>,<DM>,<Z>,<S/N>,<EPN Pulsar>,<Frequency>,<Path>,<Parent Dir>,<Size Bits>,<Size GB>,<MD5>
            #
            # As each file name should be unique, we can use <Filename> as a unique identifier.

            # Ok, so now we read the file:
            test_vector_db_content = Common.read_file(output_file)

            if test_vector_db_content is None:
                print "\t\tTest vector database empty!"

            else:
                # At least the object is not null - are there any lines of data?
                if len(test_vector_db_content) <= 0:
                    print "\t\tTest vector database empty!"
                else:
                    for line in test_vector_db_content:

                        if line is not None:

                            tv_entry_key, tv_entry_value = self.getTestVectorEntry(line)

                            if tv_entry_key is not None and tv_entry_value is not None:
                                test_vectors[tv_entry_key] = tv_entry_value
        else:
            # No pre-existing file found.
            print "\t\tNo existing test vector database file was found."

        # Output some useful debugging information.
        print "\t\tExisting test vectors found: ", str(len(test_vectors))

        # ****************************************
        #    Now check for new test vectors
        # ****************************************

        if Common.dir_exists(directory):

            print "\t\tSearching: " + directory

            # Count of the 'new' test vectors, i.e., not seen before.
            newtestVectorsFound = 0

            # Counts all the test vectors found.
            testVectorCount = 0

            # Size of all the test vectors combined in GB (gigabytes).
            totalTestVectorSizeGB = 0

            # Size of the new the test vectors combine, only, in GB (gigabytes).
            totalNewVectorSizeGB = 0

            # Counts the vectors that have changed unexpectedly.
            testVectorsThatHaveChanged = 0

            start = datetime.datetime.now()  # Used to measure processing time.

            # For each type of file this program recognises
            for filetype in fileExtensions:

                # Loop through the specified directory
                for root, subFolders, filenames in os.walk(directory):

                    # If the file type matches one of those this program recognises

                    for file_name in filenames:

                        if file_name.endswith(filetype):

                            # Increment test vector count
                            testVectorCount += 1

                            # Gets full path to the file.
                            full_file_path = os.path.join(root, file_name)

                            # Check if the test vector has already been seen.
                            if test_vectors.has_key(file_name):

                                print "\t\tTest vector already seen: ", file_name

                                # Check the file hasn't changed. To do this, compare the file
                                # size in bits, the the number of bits we previously recorded
                                # in the test vector database file.
                                current_size_bits = int(Common.file_size_bits(full_file_path))

                                test_vector_parameters = test_vectors[file_name]
                                previous_size_bits = test_vector_parameters[10]# Index 11-1 has the number of bits

                                # Update stats
                                totalTestVectorSizeGB += DataConversions.convertBitToByte(current_size_bits, 'GB')

                                if int(current_size_bits) != int(previous_size_bits):
                                    testVectorsThatHaveChanged += 1
                                    print "\t\tTest vector has changed: ", file_name

                                    # Keep details of the vector/s that have changed unexpectedly.
                                    changed_vectors[file_name] = test_vector_parameters
                            else:

                                outcome, size_in_gb = self.record(full_file_path, root, file_name, output_file, output_format)

                                totalTestVectorSizeGB += size_in_gb

                                if outcome:

                                    newtestVectorsFound += 1
                                    totalNewVectorSizeGB += size_in_gb

            # Finally get the time that the procedure finished.
            end = datetime.datetime.now()

            print "\t\tCompleted file search."
            print "\t\tTotal test vectors found: ", str(testVectorCount)
            print "\t\tTotal test vector size (GB): ", str(totalTestVectorSizeGB)
            print "\t\tNew test vectors found: ", str(newtestVectorsFound)
            print "\t\tTotal new test vector size (GB): ", str(totalNewVectorSizeGB)
            print "\t\tTest vectors unexpectedly different: ", str(testVectorsThatHaveChanged)

            # Print out those vectors that have changed.
            if testVectorsThatHaveChanged > 0:
                for key, value in changed_vectors.iteritems():
                    print "\t\t\tTest vector now different size: ", str(key)

            print "\t\tExecution time: ", str(end - start)
            print "\t\tDone searching directory."

        else:
            print "\t\tNo valid test vector directory supplied"

    # ****************************************************************************************************

    def record(self, full_file_path, parent, file_name, output_path, output_format):
        """
        Records the file found in the parsed directory. This function is only
        used during testing.

        Parameters
        ----------
        :param full_file_path: the full path to the file found.
        :param parent: the full path to the file found.
        :param file_name: the full path to the file found.
        :param output_path: the output path to record information to.
        :param output_format: the output format, i.e. CSV or JSON.

        Returns
        ----------
        :return: N/A.

        """

        try:
            components = file_name.split('_')

            if components is not None:

                if len(components) > 7:

                    Type   = components[0]
                    Batch  = components[1]
                    Period = components[2]
                    DM     = components[3]
                    Z      = components[4]
                    SNR    = components[5]
                    EPN    = components[6]
                    Freq   = components[7].replace('.fil', '')# Weird feature of how the vectors are made

                    #url = urllib.pathname2url(full_file_path)
                    #pathname = urllib.url2pathname(url)
                    #print url

                    # Note:
                    #
                    #
                    # A test vector often has the integrated profile of a known pulsar, inserted into it.
                    # To keep track of which profile is inserted in to each vector, the .asc files which
                    # describe the pulse profile (for a specific pulsar) are recorded in the test vector
                    # file name. This is usually recorded as, for example,
                    #
                    # J0000+0000_1400.asc
                    # J0000+0000_1400_1.asc
                    #
                    # The names above indicate that the profile of the pulsar J0000+0000 has been inserted.
                    # It also indicates that the profile was observed at 1400 MHz. Finally if the pulsar
                    # has been observed more than once at that frequency, there may be multiple .asc files.
                    # Above you can see that there are two profiles for the pulsar J0000+0000, the second
                    # profile has an additional number which differentiates it (in this case 1). This info
                    # is important for auditing, but makes it a little trickier to parse the test vector
                    # file names for useful information. This is because to extract the information, we
                    # split the file name on the underscore character for simplicity. So if we have a test
                    # vector named,
                    #
                    # FakePulsar_1_0.1_10_0.0_15_J0000+0000_1400.fil
                    #
                    # We need to keep the pulsar name, plus the 14000 value, to determine the .asc file used.
                    # We also need to retain a possible number to, as in,
                    #
                    # FakePulsar_1_0.1_10_0.0_15_J0000+0000_1400_1.fil
                    #
                    # Here we simply ad some code that does this.

                    # If there are 8 components, then the pulsar has been observed only once.
                    if len(components) == 8:
                        EPN += '_' + str(Freq)
                    elif len(components) == 9:

                        ProfileNumber = components[8].replace('.fil', '')
                        EPN += '_' + str(Freq) + '_' + str(ProfileNumber)

                    if output_format == 1:
                        return self.WriteAsCSV(Type, Batch, Period, DM, Z, SNR, EPN, Freq, full_file_path, parent, file_name, output_path)
                    elif output_format == 2:
                        return self.WriteAsJSON(Type, Batch, Period, DM, Z, SNR, EPN, Freq, full_file_path, parent, file_name, output_path)
                else:
                    print "\t\tUnknown filename format processed in record function: ", full_file_path
            else:
                print "\t\tError in the record function for file: ", full_file_path

        except Exception as e:
            print "\t\tError in the record function for file: ", full_file_path
            return False, 0

    # ****************************************************************************************************

    def WriteAsCSV(self, Type, Batch, Period, DM, Z, SNR, EPN, Freq, full_file_path, parent, file_name, output_path):
        """
        Writes data to a file in the following CSV format:

        <Filename>,<Type>,<Period (ms)>,<DM>,<S/N>,<EPN Pulsar>,<Frequency>,<Path>,<Parent Dir>,<Size Bits>,<Size GB>,<MD5>

        As each file name should be unique, we can use <Filename> as a unique identifier.

        Parameters
        ----------
        :param type: The type of the data file, i.e. fake pulsar or real pulsar example.
        :param Batch: The batch the test vector was generated in.
        :param Period: The pulse period of the fake pulsar.
        :param DM: The dispersion measure of the fake pulsar.
        :param Z: The acceleration applied to the injected signal.
        :param SNR: The S/N ratio of the fake pulsar.
        :param EPN: The profile file, extracted from EPN database data.
        :param Freq: The frequency the EPN data was observed at.
        :param full_file_path: the full path to the file found.
        :param parent: the full path to the file found.
        :param file_name: the full path to the file found.
        :param output_file: the output path to record information to.

        Returns
        ----------
        :return: N/A.

        """

        print "\t\tRecording file: ", full_file_path

        # This is the correct CSV format. Here are the index positions
        # of the data items as they should appear:
        #
        # 0  = <Filename>
        # 1  = <Batch>
        # 2  = <Type>
        # 3  = <Period (ms)>
        # 4  = <DM>
        # 5  = <Z>
        # 6  = <S/N>
        # 7  = <EPN Pulsar>
        # 8  = <Frequency>
        # 9  = <Path>
        # 10 = <Parent Dir>
        # 11 = <Size Bits>
        # 12 = <Size GB>
        # 13 = <MD5>

        # Get the size of the files
        try:
            size_in_bits = Common.file_size_bits(full_file_path)

            if size_in_bits is not None:
                if size_in_bits > 0:

                    size_in_gb = DataConversions.convertBitToByte(size_in_bits, 'GB')

                    # Now compute MD5 hash...
                    md5_value = self.generate_file_md5(full_file_path)

                    output = file_name + ',' + str(Batch) +',' + Type + ',' + Period + ',' + str(DM) + ',' + str(Z)+','
                    output += str(SNR) + ',' + EPN + ',' + str(Freq) + ',' + full_file_path + ',' + parent + ','
                    output += str(size_in_bits) + ',' + str(size_in_gb) + ',' + md5_value + '\n'

                    Common.append_to_file(output_path, output)

                    return True, DataConversions.convertBitToByte(size_in_bits, 'GB')
                else:
                    print "\t\tError recording test vector file size 0: ", file_name
                    return False, 0
            else:
                print "\t\tError recording test vector file size None: ", file_name
                return False, 0

        except Exception:
            print "\t\tError extracting MD5/size for: ", file_name
            return False, 0

    # ****************************************************************************************************

    def WriteAsJSON(self, Type, Batch, Period, DM, Z, SNR, EPN, Freq, full_file_path, parent, file_name, output_path):
        """
        Writes data to the JSON format.

        Parameters
        ----------
        :param type: The type of the data file, i.e. fake pulsar or real pulsar example.
        :param Batch: The batch the test vector was generated in.
        :param Period: The pulse period of the fake pulsar.
        :param DM: The dispersion measure of the fake pulsar.
        :param Z: The acceleration applied to the injected signal.
        :param SNR: The S/N ratio of the fake pulsar.
        :param EPN: The profile file, extracted from EPN database data.
        :param Freq: The frequency the EPN data was observed at.
        :param full_file_path: the full path to the file found.
        :param parent: the full path to the file found.
        :param file_name: the full path to the file found.
        :param output_file: the output path to record information to.

        Returns
        ----------
        :return: N/A.

        """

        print "\t\tRecording file: ", full_file_path

        # Not implemented the JSON yet.
        return self.WriteAsCSV(Type, Batch, Period, DM, Z, SNR, EPN, Freq, full_file_path, parent, file_name, output_path)

    # ****************************************************************************************************

    def getTestVectorEntry(self, line):
        """
        Parses a line of text from a test vector database file. Returns a key
        value pair describing the test vector file.

        We expect the input line of text, to be a CSV file of the following format:

        <Filename>,<Batch>,<Type>,<Period (ms)>,<DM>,<Z>,<S/N>,<EPN Pulsar>,<Frequency>,<Path>,<Parent Dir>,<Size Bits>,<Size GB>,<MD5>

        As each file name should be unique, we can use <Filename> as a unique identifier.

        Parameters
        ----------
        :param line: the text read in from the test vector database file.

        Returns
        ----------
        :return: A key value pair describing the test vector file.

        """

        #print "\t\tProcessing line: ", line

        components = line.split(',')

        if components is None:
            print "\t\tLine empty - unable to get test vector details"
            return None
        else:
            # We should get here all being well.
            if len(components) != 14:
                print "\t\tLine has incorrect structure - expecting 14 columns of data!"
                return None
            else:
                try:
                    # If we reach here, the file is in principle in the correct format.
                    # Here are the index positions of the data items as they should appear
                    # if the data is valid:
                    #
                    # 0  = <Filename>
                    # 1  = <Batch>
                    # 2  = <Type>
                    # 3  = <Period (ms)>
                    # 4  = <DM>
                    # 5  = <Z>
                    # 6  = <S/N>
                    # 7  = <EPN Pulsar>
                    # 8  = <Frequency>
                    # 9  = <Path>
                    # 10 = <Parent Dir>
                    # 11 = <Size Bits>
                    # 12 = <Size GB>
                    # 13 = <MD5>
                    key = components[0]
                    value = [components[1], components[2], components[3], components[4],
                             components[5], components[6], components[7], components[8],
                             components[9], components[10], components[11], components[12],
                             components[13]]

                    return key, value

                except Exception:# Catch all for speed.
                    print "\t\tException parsing line!"
                    return None

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
