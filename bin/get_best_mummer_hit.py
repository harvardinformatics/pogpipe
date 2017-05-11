import re
import os
import sys
import unittest

from datamodel.factory.GFFFactory import GFFFactory
from datamodel.factory.FastaFile  import FastaFile
from datamodel.Feature            import Feature

import importlib
import logging
import pprint


#####

# 1. Read in query fasta sequences

#####

# 2. Read in reference fasta sequences

#####

# 3. Read in coords file and filter for hit id alignments > 10kb

#####

# 4. Read in delta file into alignment features

#####

# 5. Get 10358 hit alignments and make into fasta sequences

#####

# 6. Print out 10358 sequence and hit alignments to it.



coordsfile = sys.argv[1]
# reffile  = sys.argv[2]
# qryfile  = sys.argv[3]
# dltfile  = sys.argv[4]

### Read query and reference sequences
#refseqs = {}
#qryseqs = {}

#seq =  ref.nextSeq()

#while seq is not None:
#    refseqs[seq['id']] = seq
#    seq = ref.nextSeq()
    
#seq =  qry.nextSeq()

#while seq is not None:
#    qryseqs[seq['id']] = seq
#    seq = qry.nextSeq()


### Read deltafile - just for 10358 right now
# delta_alns = read_deltafile(deltafile,refseqs,qryseqs)

### Read coordsfile


### For each hit > 10kb make a fasta alignment

alns       = {}

f = open(coordsfile,'r')

i = 0

for line in iter(f):
    # Skip the first 5 lines
    if i > 4:
        line   = line.rstrip('\n')
        fields =  line.split()
        
        qstart = int(fields[0])
        qend   = int(fields[1])

        hstart = int(fields[3])
        hend   = int(fields[4])

        qalnlen   = int(fields[6])
        halnlen   = int(fields[7])

        pid    = float(fields[9])
        
        qlen   = int(fields[11])
        hlen   = int(fields[12])

        qcov   = float(fields[14])
        hcov   = float(fields[15])

        qid    = fields[17]
        hid    = fields[18]

        strand = 1

        if hend < hstart:
            strand = -1
            tmp = hend
            hend = hstart
            hstart = tmp
            

        tmpgff = Feature()

        tmpgff.qid    = qid
        tmpgff.qstart = qstart
        tmpgff.qend   = qend
        tmpgff.qlen   = qlen
        tmpgff.qcov   = qcov

        tmpgff.hitattr['hid']  = hid
        tmpgff.hitattr['hstart'] = hstart
        tmpgff.hitattr['hend']   = hend
        tmpgff.hitattr['hlen']   = hlen
        tmpgff.hitattr['hcov'] = hcov

        tmpgff.pid = pid
        
        tmpgff.strand = strand

        if qid == "10358":
            print("%s\tfeature\tfeature\t%d\t%d\t%f\t%d\t.\t%s\t%d\t%d\t%f\t%f\t%f\t%d\t%d"%(tmpgff.qid,tmpgff.qstart,tmpgff.qend,tmpgff.pid,tmpgff.strand,tmpgff.hitattr['hid'],tmpgff.hitattr['hstart'],tmpgff.hitattr['hend'],tmpgff.pid,tmpgff.qcov,tmpgff.hitattr['hcov'],tmpgff.qlen,tmpgff.hitattr['hlen']))

            if qid not in alns:
                alns[qid] = {}

            if hid not in alns[qid]:
                alns[qid][hid] = []

            alns[qid][hid].append(tmpgff)

    i = i + 1



for qid in alns:

    covstats = {}

    for hid in alns[qid]:
        hcov    = 0
        qcov    = 0
        totfeat = 0
        totpid  = 0
        hlen = None
        qlen = None

        for feat in alns[qid][hid]:
            hcov += feat.hitattr['hend'] - feat.hitattr['hstart'] + 1
            qcov += feat.qend - feat.qstart + 1
            totfeat += 1
            totpid += feat.pid

            if hlen is None:
                hlen = feat.hitattr['hlen']

            if qlen is None:
                qlen = feat.qlen

        hfrac = int(100*hcov/hlen)
        qfrac = int(100*qcov/qlen)

        avpid = int(totpid/totfeat)
        print("%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d"%(qid,hid,totfeat,qcov,hcov,qfrac,hfrac,qlen,hlen,avpid))

        covstats[hid] = {}
        #covstats[hid]['feat'] = alns[qid][hid]
        covstats[hid]['hfrac'] = hfrac
        covstats[hid]['qfrac'] = qfrac
        covstats[hid]['qlen'] = qcov
        covstats[hid]['hlen'] = hcov
        covstats[hid]['avpid'] = avpid


    for (k,v) in sorted(covstats.items(), key=lambda (k, v): v['qlen'],reverse=True):
        print k,v
    for hid in covstats:
        print("%s\t%d\t%d\t%d\t%d\t%d"%(hid,covstats[hid]['qlen'],covstats[hid]['hlen'],covstats[hid]['qfrac'],covstats[hid]['hfrac'],covstats[hid]['avpid']))

f.close()

