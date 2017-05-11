import re
import os
import sys
import unittest

from datamodel.factory.GFFFactory import GFFFactory
from datamodel.factory.FastaFile  import FastaFile
from datamodel.Feature            import Feature
from datamodel.analysis.MummerDeltaFile import MummerDeltaFile

import importlib
import logging
import pprint

def read_sequences(seqfile):
    seqs = FastaFile.getSequenceDict(seqfile)

    return seqs

def read_deltafile(deltafile,rseqs,qseqs):
   ### Read deltafile - just for 10358 right now

    mdf = MummerDeltaFile(deltafile,rseqs,qseqs)
    mdf.parse()
    print "ALNS"
    print len(mdf.alns)

    for id in mdf.alns:
        print id
        for f in mdf.alns[id]:
            if f.qstart == 296422:
                print ">%s"%f.hitattr['qseq']['id']
                print f.hitattr['qseq']['seq']
                print ">%s"%f.hitattr['hseq']['id']
                print f.hitattr['hseq']['seq']



    return mdf.alns

rseqfile  = sys.argv[1]
qseqfile  = sys.argv[2]

deltafile = sys.argv[3]

print "Deltafile %s"%deltafile
qid  = '10358'
rids = ['13397','13398']

start = 121113
end   = 150246

#####

# 1. Read in query fasta sequences

qseqs = read_sequences(qseqfile)

#####

# 2. Read in reference fasta sequences

rseqs = read_sequences(rseqfile)

#####

# 3. Read in coords file and filter for hit id alignments > 10kb
# Don't need this - we know we want hits to 13397 and 13398 (for sample 5) query coords 121113 and 150246

#####

# 4. Read in delta file into alignment features

alns = read_deltafile(deltafile,rseqs,qseqs)

#####

# 5. Get 10358 hit alignments and make into fasta sequences

#####

# 6. Print out 10358 sequence and hit alignments to it.




