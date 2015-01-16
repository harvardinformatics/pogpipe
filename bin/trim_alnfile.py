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

    logging.info(" ========> trim_alnfile.py")

    logging.info("ARGS %s"%args)


    ff = FastaFile(args.fastafile)

    seqs = []

    seq = ff.nextSeq()

    if not seq['id'].startswith('7'):
      seqs.append(seq)   

    while seq is not None:

        if not seq['id'].startswith('7'):
           seqs.append(seq)   

        seq = ff.nextSeq()


    seqlen  = len(seqs[0]['seq'])
    newseqs = []


    j = 0
    while j < len(seqs):
      newseqs.append("")
      j = j + 1

    i = 0
    
    while i < seqlen:

       j     = 0;
       count = 0 

       while j < len(seqs):

          if seqs[j]['seq'][i] == '-':
            count = count + 1

          j = j+1
      

       if count < len(seqs):
         j = 0;
         while j < len(seqs):
           newseqs[j]  = newseqs[j] + seqs[j]['seq'][i]
           j = j + 1

       i = i + 1


    j = 0
    while j < len(seqs):
        print ">%s\n%s"%(seqs[j]['id'], newseqs[j])
        j = j + 1

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Extract certain seuqences from a multiply aligned fasta file and trim out gaps')

    parser.add_argument('-f','--fastafile'   , help='FastaFile to trim')
    parser.add_argument('-s','--seqids',       help='Sequence IDs to extract')
    
    args = parser.parse_args()

    main(args)

