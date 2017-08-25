"""
**************************************************************************

 PageBuilder.py

**************************************************************************
 Description:

 Builds a HTML page summarising all the SKA test vectors stored in a test
 vector database fle (csv file).

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
import datetime
from Common import Common
import os


# ******************************
#
# CLASS DEFINITION
#
# ******************************

class PageBuilder(object):
    """
    Builds the simple HTML file, describing test vectors. It assumes
    a test vector database file is provided. This is a simple CSV,
    that contains details describing each test vector file. The expected
    format is as follows:

    <Filename>,<Type>,<Period (ms)>,<DM>,<S/N>,<EPN Pulsar>,<Frequency>,<Path>,<Parent Dir>,<Size Bits>,<Size GB>,<MD5>

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

    As each file name should be unique, we can use <Filename> as a unique identifier.

    ASC Directory
    ------------------
    If this class is given access to a valid .asc directory, it will look in
    that directory for PNG images showing the pulse profile stored in each
    .asc file. For example, if there is a file,

    J0006+1834_430.asc

    Each line of this contains a numerical value. For example,

    0
    1
    2
    8
    2
    1
    0

    The values corresponding to the value of the observed pulsar's integrated pulse
    profile intensity (in a profile bin). This information was extracted from the EPN
    database. Line 1 of the file corresponds to bin 1, and line n of the file corresponds
    to bin n.

    To make the test vector website easier to use, we would like to plot these pulse
    shapes, so that users can see what sort of pulse each test vector should contain.
    The simplest way to do this, is to generate a PNG image for each .asc file. I wrote
    a script called CreatePulseProfilePng.py that does just this. That script processes
    the asc directory, and outputs PNGs. Once for each .asc file. So when parsing the asc
    directory, this script expects to find two files for each pulsar - which assumes the
    CreatePulseProfilePng.py has been run. The asc should then contain files like,

    J0006+1834_430.asc
    J0006+1834_430.png

    That way we can put the image path into the HTML we create.

    Batch Directory
    ------------------
    Test vectors should be created in batches, with specific batch parameters choices.
    We eed to keep track of these parameter values, so that the vectors are entirely
    reproducible. To ensure this information is available to those using test vectors,
    we assume there is a batch directory, containing files describing each batch. The
    files are assumed to have a simple file name structure,

    Batch_<Batch Number>.txt

    We parse the batch file here, and put the information found into the test vector
    page HTML.


    """

    # ****************************************************************************************************

    def build(self, input_file, output_file, output_format, asc_dir, batch_dir):
        """
        Reads the target directory, and records the files found which
        have the specified file extension.

        Parameters
        ----------
        :param input_file: the test vector database file to be parsed.
        :param output_file: the output path to record information to (i.e. index.html).
        :param output_format: the output format, i.e. CSV or JSON.
        :param asc_dir: path to the directory containing .asc files and their PNGs.
        :param batch_dir: path to the directory containing text files describing batches.

        Returns
        ----------
        N/A

        """

        # Counts the test vector entries read from the test vector
        # database (CSV) file.
        entriesProcessed = 0

        if Common.file_exists(input_file):

            print "\t\tReading: ", input_file

            # Used to measure processing time.
            start = datetime.datetime.now()

            # Load any available batch information from the files in
            # the batch directory.
            batch_info = self.processBatchDirectory(batch_dir)

            # read the input file
            entries = Common.read_file(input_file)

            if entries is None:
                print '\t\tTest vector database file empty!'
                return False
            else:
                # Now check there is at least 1 entry.
                if len(entries) <= 0:
                    print '\t\tTest vector database file empty!'
                    return False
                else:
                    # There must be some data available. The next part attempts
                    # to iterate over each line in the database file, and build
                    # a HTML table <td></td> item from it. This information can
                    # then be simply copied in to a HTML file.

                    html = ""

                    for test_vector in entries:

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
                        # 10  = <Parent Dir>
                        # 11  = <Size Bits>
                        # 12 = <Size GB>
                        # 13 = <MD5>

                        parameters = test_vector.split(',')

                        # Check the parameters are as we expect...
                        if parameters is None:
                            print '\t\tTest vector parameters are empty - is the file empty (empty rows)'
                            return False
                        else:
                            # Now we check there are the correct number of parameters...
                            if len(parameters) != 14:
                                print '\t\tFile has incorrect number of parameters (length', len(parameters), ')'
                                return False
                            else:
                                # If here, we should have the correct number of parameters....
                                table_data = self.createTableData(parameters, asc_dir, batch_info)

                                if table_data is not None:
                                    html += table_data
                                    entriesProcessed += 1
                                else:
                                    print '\t\tUnable to build HTML table item - some unknown error'
                                    return False

                    # Now merge the HTML file components.
                    top = Common.read_file_as_string('html_fragments/top.html')
                    middle = Common.read_file_as_string('html_fragments/middle.html')

                    # Build Batch info
                    popup_html = ''
                    popup_script = '\n<script>\n\t$(document).ready(function () {\n'
                    if batch_info is not None:
                        if len(batch_info)>0:
                            for key, value in batch_info.iteritems():
                                popup_html += value[0]
                                popup_script += value[1]

                        # Close the script
                        popup_script += '\t});\n</script>\n'


                    # Add bottom of HTML file.
                    bottom = Common.read_file_as_string('html_fragments/bottom.html')

                    INDEX_HTML = top + html + middle + popup_html + popup_script + bottom

                    # Delete output file in case it exists.
                    Common.delete_file(output_file)

                    # This is a simple fudge, allowing the page to be updated
                    # at certain keyword locations.
                    INDEX_HTML = INDEX_HTML.replace('@TOTAL@', str(entriesProcessed))

                    # Now build the output file
                    Common.append_to_file(output_file, INDEX_HTML)

                    # Finally get the time that the procedure finished.
                    end = datetime.datetime.now()

                    print "Completed file search."
                    print "Entries processed:", str(entriesProcessed)
                    print "Execution time: ", str(end - start)
                    print "Done parsing directory"

        else:
            print "No valid directory supplied"

    # ****************************************************************************************************

    def createTableData(self, parameters, asc_dir, batch_dic):
        """
        Creates a HTML string describing given a list of data items. The
        list of data items should be as follows:

        0  = <Filename>
        1 =  <Batch>
        2  = <Type>
        3  = <Period (ms)>
        4  = <DM>
        5  = <Z>
        6  = <S/N>
        7  = <EPN Pulsar>
        8  = <Frequency>
        9  = <Path>
        10 = <Parent Dir>
        11 = <Size Bits>
        12 = <Size GB>
        13 = <MD5>

        The function should produce a string of the form,
        <tr>
            <td>Fake Pulsar</td>
            <td>1</td>
            <td>4000</td>
            <td>10</td>
            <td>+1.1</td>
            <td>15</td>
            <td>J0000+0000</td>
            <td>14000</td>
            <td>FULL PATH</td>
            <td>Size in GB</td>
            <td>MD5 Hash</td>
            <td>Size in bits</td>
        </tr>

        Parameters
        ----------
        :param parameters: the parameters describing the test vector.
        :param asc_dir: path to the directory containing .asc files and their PNGs.
        :param batch_dic: a dictionary of batch information.

        Returns
        ----------
        :return: N/A.

        """

        img_path = asc_dir + "/" + parameters[7] + '.png'

        print "\t\tBuilding HTML... "

        html = "\t<tr>\n"
        html += "\t\t<td>" + parameters[2] + "</td>\n" # Type

        if batch_dic is not None:

            batch_key = 'Batch_' + parameters[1] + '.txt'
            if batch_dic.has_key(batch_key):

                batch_popup = "'#batch_pop_" + parameters[1] + "'"
                html += "\t\t<td><a href="
                html += '"#" onclick="$(' + batch_popup + ').popup'
                html += "('show');"
                html += '">' + parameters[1] + '</a></td>\n'
            else:
                print 'No batch key in batch dictionary: ', batch_key
                html += "\t\t<td>" + parameters[1] + "</td>\n"  # Batch
        else:
            html += "\t\t<td>" + parameters[1] + "</td>\n" # Batch

        html += "\t\t<td>" + parameters[3] + "</td>\n" # Period
        html += "\t\t<td>" + parameters[4] + "</td>\n" # DM
        html += "\t\t<td>" + parameters[5] + "</td>\n" # Z
        html += "\t\t<td>" + parameters[6] + "</td>\n" # SNR

        # This part puts an image in in the table cell. The image
        # shows the shape of the pulse profile.
        html += '\t\t<td><span class="flagicon"><img alt=' + parameters[7] + ' src="'
        html += img_path + '"  width="128" height="128" class="thumbborder" />&#160;</span>'
        html += parameters[7] + '</td>\n'

        html += "\t\t<td>" + parameters[8] + "</td>\n" # Frequency
        html += "\t\t<td><a href='"+parameters[9]+"'>" + parameters[0]+"</a></td>\n"  # file name
        html += "\t\t<td>" + parameters[12] + "</td>\n" # Size GB
        html += "\t\t<td>" + parameters[13] + "</td>\n" # MD5 hash
        html += "\t\t<td>" + parameters[11] + "</td>\n"  # Size bits
        html += "\t</tr>\n"

        return html

    # ****************************************************************************************************

    def processBatchDirectory(self, batch_dir):
        """
        Test vectors should be created in batches, with specific batch parameters choices.
        We eed to keep track of these parameter values, so that the vectors are entirely
        reproducible. To ensure this information is available to those using test vectors,
        we assume there is a batch directory, containing files describing each batch. The
        files are assumed to have a simple file name structure,

        Batch_<Batch Number>.txt

        This function processes this directory, and extracts useful information from the
        batch files. It returns this information as html, ready to be inserted into the
        complete test vector page.

        Parameters
        ----------
        :param batch_dir: path to the directory containing text files describing batches.

        Returns
        ----------
        :return: N/A.

        """

        batch_file_count = 0
        batch_dic = {}

        for filetype in ['.txt']:

            # Loop through the specified directory
            for root, subFolders, filenames in os.walk(batch_dir):

                # If the file type matches one of those this program recognises

                for file_name in filenames:

                    if file_name.endswith(filetype) and file_name.startswith('Batch_'):

                        # Increment test vector count
                        batch_file_count += 1

                        # Gets full path to the file.
                        full_file_path = os.path.join(root, file_name)

                        # Check if the test vector has already been seen.
                        if batch_dic.has_key(file_name):
                            print '\t\tBatch already processed: ', file_name
                        else:

                            batch_file_text = Common.read_file_as_string(full_file_path)

                            if batch_file_text is None:
                                print '\t\tBatch file empty: ', file_name
                            else:

                                # Else we can build the popups
                                popup_html = self.buildBatchPopup(file_name, batch_file_text)
                                popup_script = self.buildBatchPopupScript(file_name)

                                batch_dic[file_name] = [popup_html, popup_script]

        print '\t\tBatch files found: ', batch_file_count

        return batch_dic

    # ****************************************************************************************************

    def buildBatchPopup(self, file_name, batch_file_text):
        """
        Builds the popup HTML for a batch.

        Parameters
        ----------
        :param file_name: the batch file name.
        :param batch_file_text: the text inside the batch file.

        Returns
        ----------
        :return: a HTML string if the batch file name is valid, else an empty string.

        """
        # Here is an example of the HTML structure that must be produced.
        #
        # <div id = "batch_pop_<Batch Number>" class ="well">
        #    <h4> Batch_<Batch Number>.txt </h4>
        # <pre class ="prettyprint">
        # <code>
        #    BATCH FILE TEXT HERE.
        # </code>
        # </pre>
        # <button onclick = "$('#batch_pop_<Batch Number>').popup('hide');" class ="fade_close btn btn-default"> Close </button>
        # </div>
        #
        # Where <Batch Number> is replaced by the correct batch number from the file name.

        if file_name is None:
            print '\t\tEmpty filename passed to buildBatchPopup'
            return ''

        # Get the batch number:
        file_name_components = file_name.replace('.txt', '').split('_')

        if file_name_components is None:
            print '\t\tProblem generating popup HTML- batch file name format invalid'
            return ''
        else:
            if len(file_name_components) == 2:

                batch_number = str(file_name_components[1])

                html = '\n<div id ="batch_pop_' + batch_number + '" class ="well">\n'
                html += "\t\t<h4> " + file_name + " </h4>'\n"
                html += '<pre class ="prettyprint">\n'
                html += "<code>\n"
                html += batch_file_text
                html += "</code>\n"
                html += "</pre>\n"
                html += '<button onclick = "$('
                html += "'#batch_pop_" + batch_number + "').popup('hide');"
                html += '" class ="fade_close btn btn-default"> Close </button>\n'
                html += "</div>\n"

                return html
            else:
                print '\t\tProblem generating popup HTML - batch file name format invalid'
                return ''

    # ****************************************************************************************************

    def buildBatchPopupScript(self, file_name):
        """
        Builds the popup HTML script for a batch.

        Parameters
        ----------
        :param file_name: the batch file name.

        Returns
        ----------
        :return: a HTML string if the batch file name is valid, else an empty string.

        """

        # The script so look as follows:
        #
        # $('#batch_pop_1').popup({
        #    transition: 'all 0.3s',
        #    scrolllock: true
        # });

        if file_name is None:
            print '\t\tEmpty filename passed to buildBatchPopupScript()'
            return ''

        # Get the batch number:
        file_name_components = file_name.replace('.txt', '').split('_')

        if file_name_components is None:
            print '\t\tProblem generating popup HTML script - batch file name format invalid'
            return ''
        else:
            if len(file_name_components) == 2:

                batch_number = str(file_name_components[1])

                html = "\t\t$('#batch_pop_" + batch_number + "').popup({\n"
                html +="\t\t\ttransition: 'all 0.3s',\n"
                html += "\t\t\tscrolllock: true\n"
                html += "\t\t});\n"

                return html
            else:
                print '\t\tProblem generating popup HTML script - batch file name format invalid'
                return ''

    # ****************************************************************************************************
