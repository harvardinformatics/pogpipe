import re
import os
import sys
import unittest

ens2refseqfile = sys.argv[1]
protfile       = sys.argv[2]

# Read ensembl 2 refseq file lines are like

# Gene stable ID  Transcript stable ID    RefSeq mRNA ID  RefSeq mRNA predicted ID
# ENSG00000264452 ENST00000583496
# ENSG00000278324 ENST00000620853
# ENSG00000283502 ENST00000636749
# ENSG00000241226 ENST00000476140 RN7SL836P
# ENSG00000252604 ENST00000516795 RNU2-44P

# We need the mRNA ID to ENST conversion

enst2refseq = {}

f = open(ens2refseqfile,'r')

i = 0

for line in iter(f):
    if i > 0:
        line   = line.rstrip('\n')
        fields =  line.split('\t')

        if fields[2] != '':
            fields[2] = re.sub(r'\..*','',fields[2])
            enst2refseq[fields[1]] = fields[2]


    i = i + 1

f.close()

# Now the proteomics file
f = open(protfile,'r')

i = 0

for line in iter(f):
    line = line.rstrip('\n')
    
    if i > 0:

        fields = line.split('\t')

        enststr = fields[3]
        enststr = re.sub(r'_ENSP.*','',enststr)
        
        if enststr in enst2refseq:
            enststr = "%s_%s"%(enst2refseq[enststr],enststr)

            
        fields[3] = enststr
        print '\t'.join(fields)
    else:
        print line
    i = i + 1

f.close()
