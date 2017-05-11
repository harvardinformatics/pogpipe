import re
import os
import sys
import unittest

affs       = {}
files      = []

i = 1

while i < len(sys.argv):
    file = sys.argv[i]
    files.append(file)
    
    f = open(file,'r')

    j = 0
    for line in iter(f):
        if j > 1:
            line = line.rstrip('\n')
            fields = line.split()

            row  = int(re.sub(r'\"','',fields[0]))
            kmer = re.sub(r'\"','',fields[1])
            ocount = int(fields[2])
            prob   = float(fields[3])
            ecount = float(fields[4])
            aff    = float(fields[5])
            se     = float(fields[6])

            if kmer not in affs:
                affs[kmer] = {}

            affs[kmer][file] = aff
            
            #print "ROW %d : %s : %d : %f : %f : %f : %f"%(row,kmer,ocount,prob,ecount,aff,se)

        j = j + 1

    f.close()
    
    i = i + 1


for kmer in affs:

    vals = []

    tmpstr = kmer
    
    for file in files:
        if file in affs[kmer]:
            tmpstr += "\t" + str(affs[kmer][file])
        else :
            tmpstr += "\t0"

    print tmpstr
    
            
