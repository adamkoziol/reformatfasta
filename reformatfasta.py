#!/usr/bin/env python
import os
from glob import glob
__author__ = 'adamkoziol'


class Format(object):

    @staticmethod
    def make_path(inpath):
        """
        from: http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary \
        does what is indicated by the URL
        :param inpath: string of the supplied path
        """
        import errno
        try:
            # os.makedirs makes parental folders as required
            os.makedirs(inpath)
        # Except os errors
        except OSError as exception:
            # If the os error is anything but directory exists, then raise
            if exception.errno != errno.EEXIST:
                raise

    def strainer(self):
        """
        Find all the .fasta files in the supplied path
        """
        # Get the sequences in the sequences folder into a list. Note that they must have a file extension that
        # begins with .fa
        self.strains = sorted(glob('{}*.fa*'.format(self.sequencepath)))
        assert self.strains, 'Could not find any files with an extension starting with "fa" in {}. Please check' \
                             'to ensure that your sequence path is correct'.format(self.sequencepath)
        self.formatfasta()

    def formatfasta(self):
        """
        Reformat the .fasta files with BioPython
        """
        from Bio import SeqIO
        print('Reformatting files')
        for fasta in self.strains:
            # Store the name and extension of the .fasta file
            name, extension = os.path.basename(fasta).split('.')
            # Set the name of the formatted file
            formattedfile = os.path.join(self.formattedpath, '{}_formatted.{}'.format(name, extension))
            # Create a list to store all the records from the original .fasta file
            contigs = list()
            with open(formattedfile, 'wb') as formatted:
                for record in SeqIO.parse(open(fasta, "rU"), "fasta"):
                    # Add this record to our list
                    contigs.append(record)
                # Write all the properly formatted records to the formatted file
                SeqIO.write(contigs, formatted, 'fasta')

    def __init__(self, args):
        self.path = args.path
        self.sequencepath = os.path.join(args.sequencepath, '')
        self.formattedpath = os.path.join(self.path, 'formattedfiles', '')
        # Create the output path
        self.make_path(self.formattedpath)
        self.strains = list()
        self.strainer()

if __name__ == '__main__':
    # Argument parser for user-inputted values, and a nifty help menu
    from argparse import ArgumentParser
    import time
    # Parser for arguments
    parser = ArgumentParser(description='Produce consistently formatted .fasta files from "questionably" formatted'
                                        '.fasta files')
    parser.add_argument('path',
                        help='Specify input directory')
    parser.add_argument('-s', '--sequencepath',
                        required=True,
                        help='Path of sequence files')
    # Get the arguments into an object
    arguments = parser.parse_args()

    # Define the start time
    start = time.time()
    # Run it
    Format(arguments)
    # Print a bold, green exit statement
    print '\033[92m' + '\033[1m' + "\nElapsed Time: %0.2f seconds" % (time.time() - start) + '\033[0m'


