from argparse  import ArgumentParser
from datamodel.factory.FastaFile import FastaFile
from datamodel.factory.FastaFilter import FastaFilter
from datamodel.SeqUtils            import SeqUtils
import importlib
import logging
import os
import sys
import csv
import pprint
import re
 
from config import settings

def main(args):

    ff   = FastaFile(args.fastafile)
    seqs = []
    lens = []
    bins = {}

    seq     = ff.nextSeq()
    binsize = int(args.binsize)
    
    # 1. Number of sequences
    # 2. Array of lengths
    # 3. Median
    # 4. Bins
    # 5. Distribution
    # 6. Translate

    totlen = 0

    while seq is not None:

        lens.append(seq['len'])
        totlen = totlen + seq['len']

        bin = int(seq['len']/binsize)
        
        if bin not in bins:
            bins[bin] = 0

        bins[bin] = bins[bin] + 1

        seqs.append(seq)
        seq = ff.nextSeq()

    print bins

    sortedseqs = sorted(seqs, key = lambda k: k['len'])

    median = None
    n50    = None
    tmplen = 0

    seqnum = len(seqs)

    i = 0

    for seq in sortedseqs:
        i = i + 1

        if n50 is None and tmplen > totlen/2:
            n50 = seq['len']

        if median is None and i > seqnum/2:
            median = seq['len']
            
        print seq['len'],seq['id']
        
        tmplen = tmplen + seq['len']
    
    mean = int(totlen/seqnum)

    print("Num\t%d\tN50\t%d\tMedian\t%d\tMean\t%d"%(seqnum,n50,median,mean))

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Get basic statistics on a fasta file')

    parser.add_argument('-f','--fastafile'   , help='Input fasta file')
    parser.add_argument('-b','--binsize'     , help='Length bin size')
    
    args = parser.parse_args()

    main(args)

