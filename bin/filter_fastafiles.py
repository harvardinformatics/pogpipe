from argparse  import ArgumentParser
from datamodel.factory.FastaFile import FastaFile
from datamodel.factory.FastaFilter import FastaFilter

import importlib
import logging
import os
import sys
import csv
import pprint
import re
 
from config import settings

def main(args):

    logging.info(" ========> filter_fastafile.py")

    logging.info("ARGS %s"%args)

    ff = FastaFile(args.fastafile)
    filterstr = args.str
    seqs = []

    seq = ff.nextSeq()

    while seq is not None:
        seqs.append(seq)
        seq = ff.nextSeq()

    newseqs = FastaFilter.filterById(seqs,args.str)

    print FastaFile.toString(newseqs)

    


if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Process a multiply aligned fasta file and extract stats')

    parser.add_argument('-f','--fastafile'   , help='FastaFile to trim')
    parser.add_argument('-s','--str'   ,       help='String to filter the id on')
    
    args = parser.parse_args()

    main(args)

