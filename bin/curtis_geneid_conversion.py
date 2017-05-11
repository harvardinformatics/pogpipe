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

refseq2enst = {}

f = open(ens2refseqfile,'r')

i = 0

for line in iter(f):
    if i > 0:
        line   = line.rstrip('\n')
        fields =  line.split('\t')

        if fields[2] != '':
            fields[2] = re.sub(r'\..*','',fields[2])
            refseq2enst[fields[2]] = fields[1]

    i = i + 1

f.close()

# Now the proteomics file
f = open(protfile,'r')

i = 0

for line in iter(f):
    if i > 0:
        line = line.rstrip('\n')
        fields = line.split('\t')

        protstr = fields[10]

        tmpids = protstr.split('; ')
        
        for k,v in enumerate(tmpids):
            v = re.sub(r'\..*','',v)
            tmpids[k] = v

        for k,v in enumerate(tmpids):
            if v in refseq2enst:
                v = "%s_%s"%(v,refseq2enst[v])
                tmpids[k] = v
            
        fields[10] = '; '.join(tmpids)
        print '\t'.join(fields)
    else:
        print line
    i = i + 1

f.close()
