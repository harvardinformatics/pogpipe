import os
import sys
import unittest

from argparse  import ArgumentParser

scriptdir = os.path.dirname(os.path.realpath(__file__))

from datamodel.factory.BlatFile  import BlatFile
from datamodel.factory.FastaFile import FastaFile

from datamodel.Feature   import Feature
from datamodel.FileUtils import FileUtils

def main(args):
    
    blatobj  = BlatFile(args.blatfile)
    fastaobj = FastaFile(args.fastafile)

    # Parse the fasta file
    seqs = []
    ids  = {}

    seq = fastaobj.nextSeq()

    while seq is not None:
        seqs.append(seq)
        ids[seq['id']] = len(seq['seq'])
        seq = fastaobj.nextSeq()


    feat = blatobj.nextFeature()

    tmpfeat = []
    tmpqid  = None

    foundids  = {}
    foundhits = {}

    while feat:
        
        if tmpqid is not None and len(tmpfeat) > 0:
            if tmpqid != feat.qid:
                print
                tophit = getBestHit(tmpfeat)
                foundids[tophit.qid] = 1
                foundhits[tophit.qid] = tophit
                tmpfeat = []

        tmpfeat.append(feat)
        tmpqid = feat.qid

        feat   = blatobj.nextFeature()
    
    for id in ids:
        if id not in foundids:
            print "MISSINGID %s LEN %d"%(id,ids[id])
        else:
            tophit = foundhits[id]
            print "FOUNDID\t%d\t%d\t%d\t%s"%(tophit.pid,tophit.qcov,tophit.hcov,tophit)

def getBestHit(feat):

    qid = None

    for f in feat:
        if qid is None:
            qid = f.qid
        else:
            if f.qid != qid:
                print "ERROR: Mixed query ids for feature array [%s][%s]"%(qid,feat[f].qid)
    

    #print "Got feature array  - query id [%s],  Number of hit ids [%d]"%(qid,len(feat))

    i = 0
            
    tophit  = None
    topcov  = -1
    tophcov = -1
    toppid  = -1
            
    for tmpf in feat:

        #if i == 0:
            #print "PID\tQcov\tHcov\t" + tmpf.header_str()

        #i = i+1

        match    = tmpf.hitattr['match']
        mismatch = tmpf.hitattr['mismatch']
                
        qlen    = tmpf.qlen
        hlen    = tmpf.hlen
                
        qcov    = int(100*(match+mismatch)/qlen)
        hcov    = int(100*(match+mismatch)/hlen)
        pid     = int(100*match/(match+mismatch))
                
        #print "FEA\t%d\t%d\t%d\t%s"%(pid,qcov,hcov,tmpf)
                
        if qcov > topcov:
            #print "Found new qcov %d %d"%(qcov,topcov)
            topcov = qcov
            tophit = tmpf
            toppid = pid

            tophit.pid = pid
            tophit.qcov = qcov
            tophit.hcov = hcov

                    
        elif qcov == topcov:
            if hcov > tophcov:
                #print "Found new hcov"
                tophcov = hcov
                tophit = tmpf
                toppid = pid

                tophit.pid = pid
                tophit.qcov = qcov
                tophit.hcov = hcov




    return tophit
        
if __name__ == "__main__":      

    parser        = ArgumentParser(description = 'Parse a blat psl output file and calculate query coverage')

    parser.add_argument('-b','--blatfile'   ,  help='Blatfile to parse')
    parser.add_argument('-f','--fastafile'  ,  help='Fastafile as reference set')
    
    args = parser.parse_args()

    main(args)

