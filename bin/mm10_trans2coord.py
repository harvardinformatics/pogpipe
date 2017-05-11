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
transfile     = sys.argv[2]
gtffile       = sys.argv[3]

e2g = EnsemblToGeneFile(enstogenefile)
gtf = GTFFile(gtffile)

gtf.parse()

tf  = open(transfile)

print gtf
#print e2g.tranids

for line in tf:
    id = line.rstrip('\n')

    if id in e2g.tranids:
        print e2g.tranids[id]


