#!/usr/bin/env python3
from glob import glob
from Bio import SeqIO
import shutil
from accessoryFunctions.accessoryFunctions import *
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
        if self.split:
            self.splitter()
        else:
            self.formatfasta()

    def formatfasta(self):
        """
        Reformat the .fasta files with BioPython
        """
        printtime('Reformatting files', self.start)
        for fasta in self.strains:
            # Store the name and extension of the .fasta file
            name, extension = os.path.basename(fasta).split('.')
            # Set the name of the formatted file
            formattedfile = os.path.join(self.formattedpath, '{}_formatted.{}'.format(name, extension))
            # Create a list to store all the records from the original .fasta file
            contigs = list()
            with open(formattedfile, 'w') as formatted:
                if self.unique:
                    # Create a dictionary to store the unique sequence records
                    unique = dict()
                    # Make a log file to store the duplicate
                    logfile = os.path.join(self.logs, os.path.basename(fasta))
                    # Use BioPython to create a list of sequence records
                    records = list(SeqIO.parse(fasta, 'fasta'))
                    # Convert the list of sequence to a dictionary - we'll need both; one for sorting, one for searching
                    record_dict = SeqIO.to_dict(records)
                    # Create a list of the sequence names from the sequence records
                    # Sort the list based on the on the last part of the sequence name e.g.
                    # stx1a:13:M19473:13 comes before stx1a:6:SEQ:1082
                    ids = sorted([record.id for record in records], key=lambda x: int(x.split(':')[3]))
                    # Iterate through the sorted names
                    for record in ids:
                        # Check to see if the sequence is in the dictionary of unique sequences
                        if str(record_dict[record].seq) not in unique:
                            # If it isn't in the dictionary, add the sequence as the key, and the name as the value
                            unique[str(record_dict[record].seq)] = record_dict[record].id
                            # Add this record to our list
                            contigs.append(record_dict[record])
                        # Duplicates are not added to the list of contigs
                        else:
                            # Open the log file, and write the name of the duplicate, as well as the name of the
                            # original
                            with open(logfile, 'a') as log:
                                log.write('{} duplicate of {}\n'.format(record_dict[record].id,
                                                                        unique[str(record_dict[record].seq)]))
                else:
                    for record in SeqIO.parse(open(fasta, "rU"), "fasta"):
                        # Add this record to our list
                        contigs.append(record)
                # Write all the properly formatted records to the formatted file
                SeqIO.write(contigs, formatted, 'fasta')

    def splitter(self):
        """
        Correctly format FASTA files, and write individual records to files
        """
        printtime('Reformatting and splitting files', self.start)
        self.make_path(self.splitpath)
        for fasta in self.strains:
            if self.unique:
                logfile = os.path.join(self.logs, os.path.basename(fasta))
                unique = dict()
                # Get the sequence records from the file into a list, as well as a dictionary
                records = list(SeqIO.parse(fasta, 'fasta'))
                record_dict = SeqIO.to_dict(records)
                # Create a list of the sequence names from the sequence records
                # Sort the list based on the on the last part of the sequence name e.g.
                # stx1a:13:M19473:13 comes before stx1a:6:SEQ:1082
                ids = sorted([record.id for record in records], key=lambda x: int(x.split(':')[3]))
                for record in ids:
                    if str(record_dict[record].seq) not in unique:
                        unique[str(record_dict[record].seq)] = record_dict[record].id
                        # Create the file name
                        filename = os.path.join(self.splitpath, record_dict[record].id + '.fa')
                        # Open the FASTA file and write the record to it
                        with open(filename, 'w') as split:
                            SeqIO.write(record_dict[record], split, 'fasta')
                    else:
                        with open(logfile, 'a') as log:
                            log.write('{} duplicate of {}\n'.format(record.id, unique[str(record.seq)]))
            else:
                for record in SeqIO.parse(open(fasta, "rU"), "fasta"):
                    # Create the file name
                    filename = os.path.join(self.splitpath, record.id + '.fa')
                    # Open the FASTA file and write the record to it
                    with open(filename, 'w') as split:
                        SeqIO.write(record, split, 'fasta')

    def __init__(self, args):
        self.path = args.path
        self.start = args.start
        self.sequencepath = os.path.join(args.sequencepath, '')
        self.formattedpath = os.path.join(self.path, 'formattedfiles', '')
        self.splitpath = os.path.join(self.path, 'splitfiles')
        self.logs = os.path.join(self.path, 'logs')
        make_path(self.logs)
        self.split = args.split
        self.unique = args.unique
        if self.unique:
            try:
                shutil.rmtree(self.logs)
            except IOError:
                pass
            self.make_path(self.logs)
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
    parser.add_argument('-S', '--split',
                        action='store_true',
                        help='Split a multifasta into individual files')
    parser.add_argument('-u', '--unique',
                        action='store_true',
                        help='Remove duplicate sequences when formatting the .fasta files')
    # Get the arguments into an object
    arguments = parser.parse_args()

    # Define the start time
    arguments.start = time.time()
    # Run it
    Format(arguments)
    # Print a bold, green exit statement
    print('\033[92m' + '\033[1m' + "\nElapsed Time: %0.2f seconds" % (time.time() - arguments.start) + '\033[0m')
