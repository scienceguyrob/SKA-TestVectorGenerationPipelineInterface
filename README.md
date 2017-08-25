# SKA-TestVectorGenerationPipelineInterface (version 1.0)
A collection of Python scripts used to automatically generate a HTML web interface, for the test vectors created using the
[SKA Test Vector Generation Pipeline](https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline). The test vectors
are simply files containing realistic pulsar signals, used to test the prototype code created during the design phase of
the SKA telescope.

## Author: Rob Lyon
## Email : robert.lyon@manchester.ac.uk
## web   : www.scienceguyrob.com

### Overview
This repository consists of, 

* Python scripts that generate a webpage describing available test vectors, given appropriate inputs.
* Images and other resources that support the webpage. 

### Context
After running the pipeline code provided [here](https://github.com/scienceguyrob/SKA-TestVectorGenerationPipeline) there
should be one or more test vectors stored in a directory somewhere on a suitable server. Each test vector will be stored
as a '.fil' file, otherwise known as a filterbank file. A user may generate hundreds or thousands of test vectors. It can
be difficult to keep track of which test vectors are available, and what each contains. This is because each test vector
is generated using a set of input parameters for which there are literally billions of possibilities (i.e. choice of
pulse to be injected into the test vector, the pulsar parameters, the test vector size etc.). The code provided here helps
make it easier to manage the test vectors, by producing an interactive webpage describing them. The page is produced by
parsing the directory containing test vectors, extracting their details, and then forming a webpage containing this 
information. In principle this is simple to do, though it is fiddly. The code provided here assumes a user has one or
more test vectors siting in a directory somewhere, for which they would like a nice summary webpage.

### HTML Generation Scripts & Support Scripts

1. A test vector directory parser.

    There are two scripts involved in this process:

	TestVectorDirectoryParser.py
	TestVectorDirectoryParserApp.py

	You should only execute the TestVectorDirectoryParserApp.py script directly.

	Together, these have a couple of jobs.

	* To determine what test vectors are available for use.
	* To collect their details, via extracting information from their file names.
	* To compute the MD5 hash and file size of each test vector, and determine the software versions used to generate them.
	* To persist this information in some way, so that it can be quickly accessed.

	The test vector directory parser simply reads in a path to a test vector directory, and outputs a file summarising
	all the available test vectors. Whilst it is simple in principle, it needs some basic logic - i.e. as it computes MD5
	hashes for each test vector it finds, it needs to avoid recomputing hashes for files already seen. This is because it
	is computationally expensive to compute MD5 hashes for very large files. Especially when the test vectors can be up
	to 36GB in size. Thus, this application must know which vectors it has seen before, and which it hasn't.

	All this information should be stored in a test vector database file. We use a simple CSV based file for convenience.

2. A script that builds images describing the shape of an EPN data file pulse.

    The script CreatePulseProfilePng.py reads a directory filled with .asc files, and create plots using Matplotlib.
	The plots are written out to a PNG file. These PNGs are then used during the HTML page building process, to provide
	a visual indication of what type of pulse is in each test vector.

3. A HTML page building application.

    There are two scripts involved in this process:

	PageBuilder.py
	PageBuilderApp.py

	You should execute the PageBuilderApp.py script.

	Together, these have a couple of jobs.

	The scripts read the test vector database file, and use this information to build a working summary webpage. As
	I didn't want to get into the nitty gritty of web-design for such a simple page, I recycled old code.

	I took a webpage I built in the past, which had a simple table structure which was easy to view. This table is
	dynamic, and has nice search features. So using it makes it easy to search for test vectors. To make this work,
	all we need to do is replace the original table data HTML, with new table data HTML describing the test vectors.

	The code simply splices together old HTML, with dynamically generated table data entries (based on the data in
	the test vector database file), producing a working webpage.

### Hosting

Once the scripts described above have been executed, you should have a simple HTML webpage - but how to host it? The easiest
way to host the site, is to use the inbuilt python webserver. Simply navigate to the root of the test vector directory
structure, and execute,

```
python -m SimpleHTTPServer <PORT NUMBER>
```

Where <PORT NUMBER> is a port of your choice.

### Pre-requisites
Python 2.7 or later. Matplotlib and Numpy are also recommended.

### Usage

The scripts must be executed in order. We assume all files necessary to build the site, sit at the top level of the
directory structure which holds the test vectors. This includes all the files in this distribution.

The following steps must be taken.

1. Move the contents of the 'src' directory, to the ROOT directory that contains all the test vectors. This means all
python scripts, sub-directories (data,vendor etc), and all HTML content must be moved there.

2. Execute the CreatePulseProfilePng.py script on the directory containing .asc files, if the PNG images describing
pulse profile shapes have not been created. These images are inserted into the test vector webpage, making it easier
for users to know what sort of pulse shape to expect in each test vector. Also make sure the batch directory exists,
which contains files describing the process of batch creation. The expected format for the batch file names: 

```
Batch_<Batch Number>.txt.
```

2. Once the files are in place, execute the TestVectorDirectoryParserApp.py. It must be told where to look for the test
vectors. For example,
        
```
python TestVectorDirectoryParserApp.py --dir data/vectors --out TestVectorDB.csv -v
```

3. Executing the above application, will produce an output CSV file, that describes all the test vectors. Next the 
PageBuilderApp.py is executed. It reads in the CSV file, and outputs a valid HTML file that summarises all the test
vectors. It can be run as follows,
        
```
python PageBuilderApp.py --in TestVectorDB.csv --out index.html --asc data/asc --batch data/batch
```

4. Now the index.html page can be opened in a browser, and the test vectors viewed.


### Acknowledgements

This work used the Dynatable plugin (http://www.dynatable.com/) to create the interactive table, and the jQuery Popup
Overlay plugin (http://dev.vast.com/jquery-popup-overlay/) to create reference popups. Thanks to both for their work!!


### Change log

N/A