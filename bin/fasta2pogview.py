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
    stub = args.stub

    flen = open(stub+".chrlen",'w')
    blen = open(stub+ '.cytoband.txt','w')

    seq = ff.nextSeq()


    while seq is not None:
        flen.write("%s\t%d\n"%(seq['id'],seq['len']))
        blen.write("%s\t0\t%d\tband0\tband0\n"%(seq['id'],seq['len']))
        seq = ff.nextSeq()

    flen.close()
    blen.close()


if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Extract contig/chromosome lengths from fasta and create pogview chr and band files')

    parser.add_argument('-f','--fastafile'   , help='FastaFile to process')
    parser.add_argument('-s','--stub'   ,       help='Filename stub for the pogview files')
    
    args = parser.parse_args()

    main(args)

