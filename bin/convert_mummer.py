from argparse  import ArgumentParser

import importlib
import logging
import os
import sys
import csv
import pprint

"""
*** .delta OUTPUT ***   

This output file is a representation of the all-vs-all alignment between the sequences contained in the multi-FASTA input files. 
It catalogs the coordinates of aligned regions and the distance between insertions and deletions contained in these alignment regions. 

The first two lines of the file are identical to the .cluster output. 

The first line lists the two original input files separated by a space.
The second line specifies the alignment data type, either "NUCMER" or "PROMER". 

Every grouping of alignment regions have a header, just like the cluster's header in the .cluster file. 
This is a FASTA style header and lists the two sequences that produced the following alignments after a '>' and separated by a space.
After the two sequences are the lengths of those sequences in the same order. 

An example header might look like: >tagA1 tagB1 500 2000000   

Following this sequence header is the alignment data. 

Each alignment region has a header that describes the start and end coordinates of the alignment in each sequence. 
These coordinates are inclusive and reference the forward strand of the current sequence. 

Thus, if the start coordinate is greater than the end coordinate, the alignment is on the reverse strand. 

The four digits are the start and end in the reference sequence respectively and the start and end in the query sequence respectively. 

These coordinates are always measured in DNA bases regardless of the alignment data type. 

The three digits after the starts and stops are: 
   the number of errors (non-identities), 
   similarity errors (non- positive match scores) 
   non-alpha characters in the sequence (used to count stop-codons i promer data). 

An example header might look like: 5198 22885 5389 23089 20 20 0    

Each of these headers is followed by a string of signed digits, one per line, with the final line before the next header equaling 0 (zero). 

Each digit represents the distance to the next insertion in the reference (positive int) or deletion in the reference (negative int), 
as measured in DNA bases or amino acids depending on the alignment data type.

For example, with 'nucmer' the delta sequence (1, -3, 4, 0) would represent 
    - an insertion at positions 1 and 7 in the reference sequence and 
    - an insertion at position 3 in the query sequence. 

Or with letters: A = acgtagctgag$ B = cggtagtgag$ Delta = (1, -3, 4, 0) A = acg.tagctgag$ B = .cggtag.tgag$   

Using this delta information, it is possible to re-generate the alignment calculated by 'nucmer' or 'promer' as is done in the 'show-coords' program. 

This allows various utilities to be crafted to process and analyze the alignment data using a universal format. 

Below is what a .delta file might look like: 

/home/username/reference.fasta /home/username/query.fasta 
NUCMER 
>tagA1 tagB1 500 2000000 
88 198 1641558 1641668 0 0 0 
0
167 4877 1 4714 15 15 0 
2456 
1 
-11 
769 
950 
1 
1 
-142 
-1 
0 
>tagA2 tagB4 50000 30000 
5198 22885 5389 23089 18 18 0 
-6 
-32 
-1 
-1 
-1 
7 
1130 
0
"""

scriptdir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptdir + "/../")

from datamodel.factory.FastaFile              import FastaFile


def main(args):

    logging.info(" ========> Converting mummer delta format for %s %s %s"%(args.deltafile,args.reffile,args.queryfile))

    logging.info("ARGS %s"%args)


    ref = FastaFile(args.reffile)
    qry = FastaFile(args.queryfile)

    print ref
    print qry

    refseqs = {}
    qryseqs = {}

    seq =  ref.nextSeq()

    while seq is not None:
        refseqs[seq['id']] = seq
        seq = ref.nextSeq()

    seq =  qry.nextSeq()

    while seq is not None:
        qryseqs[seq['id']] = seq
        seq = qry.nextSeq()


    fh = open(args.deltafile)

    alns = {}
    lnum = 0

    line = fh.readline()

    while line != "":   # Can't use for line in fh: because we read the alignment in chunks

        lnum = lnum + 1

        line = line.rstrip('\n')
        ff   = line.split(' ')


        if lnum == 1:

            """  The first line lists the two original input files separated by a space."""

            if1 = ff[0]
            if2 = ff[1]

            print "Input files [%s][%s]"%(if1,if2)


        elif lnum == 2:

            """ The second line specifies the alignment data type, either NUCMER or "PROMER"""

            alntype = ff[0]

            if alntype != "NUCMER":
                raise Exception("Only NUCMER alignments are currently parsed - we have [%s]"%alntyp)


        else:

            """ Every grouping of alignment regions have a header, just like the cluster's header in the .cluster file. 
            This is a FASTA style header and lists the two sequences that produced the following alignments after a '>' and separated by a space.
            After the two sequences are the lengths of those sequences in the same order. 
            
            An example header might look like: >tagA1 tagB1 500 2000000   """

            if ff[0].startswith(">"):
                id1 = ff[0].replace(">",'')
                id2 = ff[1]
                
                len1 = int(ff[2])
                len2 = int(ff[3])

                print "IDs %s %s %d %d"%(id1,id2,len1,len2)

                """ The four digits are the start and end in the reference sequence respectively and the start and end in the query sequence respectively. 

                These coordinates are always measured in DNA bases regardless of the alignment data type. 
                
                The three digits after the starts and stops are: 
                the number of errors (non-identities), 
                similarity errors (non- positive match scores) 
                non-alpha characters in the sequence (used to count stop-codons i promer data). 
                
                An example header might look like: 5198 22885 5389 23089 20 20 0  """

                tmpline  = fh.readline()
                tmpline  = tmpline.rstrip('\n')
                tmpff    = tmpline.split(' ')

                rstart   = int(tmpff[0])
                rend     = int(tmpff[1])
                qstart   = int(tmpff[2])
                qend     = int(tmpff[3])

                errors   = int(tmpff[4])
                simerrs  = int(tmpff[5])
                nonalpha = int(tmpff[6])
                
                if id1 not in refseqs:
                    raise Exception("Can't find reference sequence [%s] in ref file [%s]"%(id1,reffile))

                if id2 not in qryseqs:
                    raise Exception("Can't find query sequence [%s] in query file [%s]"%(id2,queryfile))
                rseq = refseqs[id1]
                qseq = qryseqs[id2]
        
                #print "Found alignment header %s %d %d ::  %s %d %d"%(id1,rstart,rend,id2,qstart,qend)

                """ Each of these headers is followed by a string of signed digits, one per line, with the final line before the next header equaling 0 (zero). 

                Each digit represents the distance to the next insertion in the reference (positive int) or deletion in the reference (negative int), 
                as measured in DNA bases or amino acids depending on the alignment data type.
                
                For example, with 'nucmer' the delta sequence (1, -3, 4, 0) would represent 
                - an insertion at positions 1 and 7 in the reference sequence and 
                - an insertion at position 3 in the query sequence. 
                
                Or with letters: A = acgtagctgag$ B = cggtagtgag$ Delta = (1, -3, 4, 0) A = acg.tagctgag$ B = .cggtag.tgag$    """

                count = fh.readline()
                count = count.rstrip('\n')
                count = int(count)

                tmprseq = rseq['seq']
                tmpqseq = qseq['seq']

                if rend > rstart:
                    tmprseq = tmprseq[rstart-1:rend-1]
                else:
                    tmprseq = tmprseq[rend:rstart]
                    tmprseq = reverse_complement(tmprseq)


                if qend > qstart:
                    tmpqseq = tmpqseq[qstart-1:qend-1]
                else:
                    tmpqseq = tmpqseq[qend:qstart]
                    tmpqseq = reverse_complement(tmpqseq)

                insertpos = 0

                while count != 0:
                    if count < 0:
                        """ This is an insertion in the query sequence so we put a - in the ref"""
                        
                        insertpos = insertpos + abs(count)
                        tmprseq = tmprseq[:insertpos-1] + "-" + tmprseq[insertpos-1:]

                    elif count > 0:
                        """ This is an insertion in the reference sequence """
                        insertpos = insertpos + abs(count)
                        tmpqseq = tmpqseq[:insertpos-1] + "-" + tmpqseq[insertpos-1:]

                    
                    count = fh.readline()
                    count = count.rstrip('\n')
                    count = int(count)

                seq1 = {}
                seq2 = {}
                seq1['id'] = id1
                seq2['id'] = id2
                seq1['seq'] = tmprseq
                seq2['seq'] = tmpqseq


                print prettyPrint([seq1,seq2])
                
                if id1 not in alns:
                    alns[id1] = []

                alns[id1].append([seq1,seq2])

        line = fh.readline()

    
    for id in alns:
        print id
        for (seq1,seq2) in alns[id]:
            print "%s - %s"%( seq1['id'],seq2['id'])


def prettyPrint(seqs):

    outstr = ""
    str = []
    
    j = 0;
    
    while j < len(seqs):

        tmpstr = []
        i = 0
        
        while i < len(seqs[j]['seq']):

            c = seqs[j]['seq'][i]

            if j > 0 and i < len(seqs[0]['seq']) and c == seqs[0]['seq'][i]:
                tmpstr.append('.')
            else:
                tmpstr.append(c)
              
            i = i+1

        str.append(tmpstr)
          
        j = j + 1


    i = 0

    while i < len(seqs[0]['seq']):
        j = 0 

        while j < len(seqs):
            outstr = outstr + "%40s %s\n"%(seqs[j]['id'],''.join(str[j][i:i+80]))
            j = j + 1

        outstr = outstr +  "\n" 
        i = i + 80

    return outstr

def reverse_complement(seqstr):

    comps = {}
    comps['A'] = 'T'
    comps['T'] = 'A'
    comps['G'] = 'C'
    comps['C'] = 'G'
    comps['a'] = 't'
    comps['t'] = 'a'
    comps['g'] = 'c'
    comps['c'] = 'g'

    i = 0
    newstr = ""
    while i < len(seqstr):
        ch = seqstr[i]

        if ch in comps:
            newstr = newstr +  comps[ch]

        i = i + 1

    return newstr[::-1]

        
if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Convert mummer delta format to fasta')

    parser.add_argument('-d','--deltafile'   , help='The mummer delta output file .delta')
    parser.add_argument('-r','--reffile'     , help="The input reference fasta file")
    parser.add_argument('-q','--queryfile'   , help="The input query fasta file")
    
    args = parser.parse_args()

    main(args)

