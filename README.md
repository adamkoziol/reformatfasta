# reformatfasta

Reformat .fasta files using BioPython

# Installation

Clone the repository:

`git clone https://github.com/adamkoziol/reformatfasta.git`

Install python dependencies:

	
```
cd reformatfasta/
python setup.py install
```

# Usage

### Example command

`python reformatfasta.py path -s path/to/sequences`

##### Required arguments:

* path to the folder to be used to store results
* -s: path to folder containing sequences. I normally set this to be /path/sequences

##### Optional arguments:

* -S: Split a multifasta file into properly formatted individual files
* -u: Remove duplicate sequences (duplicates are interpreted as identical at the sequence level; 
the name of the sequence is not taken into account) 

See usage below:

```
usage: reformatfasta.py [-h] -s SEQUENCEPATH [-S] [-u] path

Produce consistently formatted .fasta files from "questionably"
formatted.fasta files

positional arguments:
  path                  Specify input directory

optional arguments:
  -h, --help            show this help message and exit
  -s SEQUENCEPATH, --sequencepath SEQUENCEPATH
                        Path of sequence files
  -S, --split           Split a multifasta into individual files
  -u, --unique          Remove duplicate sequences when formatting the .fasta
```