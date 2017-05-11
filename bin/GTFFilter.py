""" Takes ucsc ensemblToGene.txt file and gtf file and converts ensembl transcript ids to gene names.  outputs gff"""
import os
import sys
import re
import unittest

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.GTFFile           import GTFFile

from datamodel.FileUtils import FileUtils


gtffile       = sys.argv[1]
idfile        = sys.argv[2]


id_fh = open(idfile,"r")

ids = {}

for line in id_fh:
    id = line.rstrip('\n')
    ids[id] = 1


gtf_fh = open(gtffile,"r")

for line in gtf_fh:
    line = line.rstrip('\n')

    fields = line.split('\t')
    
    tmp = fields[8]

    tmp = re.sub(r'.*transcript_id "(.*)";',r'\1',tmp)

    if tmp in ids.keys():
        print line 
