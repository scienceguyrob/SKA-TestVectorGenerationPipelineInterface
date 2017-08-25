**************************************************************************
|                                                                        |
|  Data_Readme.txt                                                       |
|                                                                        |
**************************************************************************
| Author: Rob Lyon                                                       |
| Email : robert.lyon@manchester.ac.uk                                   |
| web   : www.scienceguyrob.com                                          |
**************************************************************************

This directory contains sub-directories of data, crucial to generating
the test vector website. I describe these sub-directories below.


ASC Directory
--------------------------------------------------------------------------

This directory contains files which describe pulse profiles extracted from
the EPN database. Each file is named as follows:

<Pulsar name>_<Frequency>.asc

Where <Pulsar name> is the pulsar 'J' name, and <Frequency> the observation
frequency of the EPN data. Each .asc file is accompanied by a PNG image,
which shows the shape of the pulse in the file.

There is a single file per each unique entry in the EPN database, representing
observations covering a wide range of frequencies. The files themselves are
in a simple column vector format. They contain the total pulse intensity
observed (the I stokes parameter), where the value of each bin is written to
a separate line in an individual file.

For example:

0
1
2
3
11
29
67
180
71
39
9
2
1
1
1
0

has 16 bins, each describing total pulse intensity.

Note:

The intensity values stored in the files are scaled a [0,255] range.

This data was created with a python script, EpnToAsc.py,  which converts
EPN files saved from the EPN database, to .asc files which describe pulsar
pulse profiles. Data was extracted from the EPN database on March 15th 2016.


batches Directory
--------------------------------------------------------------------------

This contains batch files. These describe the steps applied when generating
a batch of SKA test vectors. Each batch file should be named as follows:

<Batch>_<Batch number>.txt

Where <Batch number> corresponds to the batch in question, i.e.

Batch_1.txt, Batch_2.txt etc.

The directory contains an example batch file.

Batch files are needed for test vector website to correctly link to the
batch each test vector was generated in.


vectors Directory
--------------------------------------------------------------------------

This directory contains some example files that mimic test vectors. These
are not proper test vectors, and thus should not be processed in practice.
They are simply used here for testing.