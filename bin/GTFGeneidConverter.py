""" Takes ucsc ensemblToGene.txt file and gtf file and converts ensembl transcript ids to gene names.  outputs gff"""
import os
import sys
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.EnsemblToGeneFile import EnsemblToGeneFile
from datamodel.factory.GTFFile           import GTFFile

from datamodel.FileUtils import FileUtils


enstogenefile = sys.argv[1]
gtffile       = sys.argv[2]

e2g = EnsemblToGeneFile(enstogenefile)

gtf = GTFFile(gtffile)

geneid = gtf.nextGene()

while geneid:

    trans = gtf.genes[geneid]

    print "Got transcripts for gene [%s] [%d]"%(geneid,len(trans))
    
    for tran in trans:

        newgeneid = tran + "_" + tran

        if e2g.tranids.has_key(tran):
            newgeneid = e2g.tranids[tran].keys()[0] + "_" + tran
            print "Got new geneid [%s][%s]"%(newgeneid,tran)
        
        for ex in trans[tran]:
            ex.hid = newgeneid
            print ex
    geneid = gtf.nextGene()


