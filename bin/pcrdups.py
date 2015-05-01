from argparse  import ArgumentParser

import importlib
import logging
import os
import sys
import csv
import pprint
import re
import random
 
def main(args):

    beads = int(float(args.beads))
    mols  = int(float(args.unique_molecules))
    pcr   = int(args.pcr_molecules)

    print "Beads %d"%beads
    print "Mols %d"%mols
    print "PCR %d"%pcr

    counts = {}

    i = 0

    # Chance of hitting a bead is mols * pcr / beads

    phit = float(beads*1.0/(pcr*mols))

    print "Phit %f"%phit

    while i < mols:
        
        j = 0
        while j < pcr:
            tmp = random.randint(0, 100000)

            if (tmp < int(phit*100000)):
                #print "Found %d %d %d %d"%(i,j,tmp,int(phit*100000))
                if i not in counts:
                    counts[i] = 1
                else:
                    counts[i] = counts[i] + 1
                    
                    print "Found dup %d %d %d"%(i,j,tmp)
                    print "Counts %d %d"%(len(counts),i)
                    process_counts(counts)
                    
            j = j + 1
        
        i = i + 1

    print counts

def process_counts(counts):
    
    tots = {}

    for tmp in counts:
        #print "TMP %d"%tmp
        count = counts[tmp]
        if count not in tots:
            tots[count]  = 1
        else:
            tots[count] = tots[count] + 1

    print tots
        
    
if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Simulate how many PCR duplicates are generated')

    parser.add_argument('-u','--unique_molecules'   , help='Number of unique molecules')
    parser.add_argument('-b','--beads'              , help='Number of beads (reads)')
    parser.add_argument('-p','--pcr_molecules'      , help='Number of times the molecules are duplicated by PCR')
    
    args = parser.parse_args()

    main(args)

