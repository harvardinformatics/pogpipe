from argparse  import ArgumentParser
from datamodel.factory.FastaFile import FastaFile

import importlib
import logging
import os
import sys
import csv
import pprint
import re
 
from config import settings

def main(args):

    logging.info(" ========> process_alnfile.py")

    logging.info("ARGS %s"%args)

    ff = FastaFile(args.fastafile)

    seqs = []

    seq = ff.nextSeq()

    #  We first want to flag which sequences are present and which are not
    #  get the ids
    #  sort alphbetically
    #  print the ids joined together

    #  We then want to get some stats on the alignment
    #  Number of sequences
    #  Length 
    #  Coverage for each sequence
    #  Get consensus
    #  PID to consensus for each sequence
    #  Mismatches for each sequence

    #  We then want some specifics
    #  Positions where 2 sequences are the same and the other is not
  
    ids = [] 

    while seq is not None:
        ids.append(seq['id'])
        seq = ff.nextSeq()

    print "\nFILESTATS\t%s\tNumber_of_seqs\t%d\tIDS\t%s"%(args.fastafile,len(ids),','.join(ids))


    stats = ff.calcStats()


if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Process a multiply aligned fasta file and extract stats')

    parser.add_argument('-f','--fastafile'   , help='FastaFile to trim')
    
    args = parser.parse_args()

    main(args)

