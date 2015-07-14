from argparse  import ArgumentParser

from datamodel.factory.GFFFactory import GFFFactory
from datamodel.factory.FastaFile  import FastaFile
from datamodel.Feature            import Feature

import importlib
import logging
import os
import sys
import csv
import pprint


standardCodonTable = {'name': 'Standard',
                      'alt_name': 'SGC0', 
                      'id': 1,
                      'table': {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S',
        'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'TAT': 'Y', 'TAC': 'Y',
        'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CTT': 'L', 'CTC': 'L',
        'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P',
        'CCG': 'P', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I',
        'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'ACT': 'T', 'ACC': 'T',
        'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K',
        'AAG': 'K', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A',
        'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 'GAC': 'D',
        'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
        'GGG': 'G', },
                      'stop_codons': ['TAA', 'TAG', 'TGA', ],
                      'start_codons': ['TTG', 'CTG', 'ATG', ]
                      }

"""

Notes - need to turn the alignments into gffs - then need to overlap the annotation gffs with the alignment gffs


"""


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
    gff = GFFFactory(args.gfffile)

    g   = gff.nextGFF()

    gffs = {}

    while g is not None:

        if g.type2 == "CDS":
            #print "QID %s %s"%(g.qid,g.type2)
            if g.qid not in gffs:
                gffs[g.qid] = []

            gffs[g.qid].append(g)

        g = gff.nextGFF()

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

    id1  = None
    id2  = None
    len1 = None
    len2 = None


    while line != "":   # Can't use for line in fh: because we read the alignment in chunks

        lnum = lnum + 1

        line = line.rstrip('\n')
        ff   = line.split(' ')


        if lnum == 1:

            """  The first line lists the two original input files separated by a space."""

            if1 = ff[0]
            if2 = ff[1]

            print "Input files [%s][%s]\n"%(if1,if2)


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

                #print "IDs %s %s %d %d"%(id1,id2,len1,len2)

            else:
                #print "Parsing %s"%line
                """ The four digits are the start and end in the reference sequence respectively and the start and end in the query sequence respectively. 

                These coordinates are always measured in DNA bases regardless of the alignment data type. 
                
                The three digits after the starts and stops are: 
                the number of errors (non-identities), 
                similarity errors (non- positive match scores) 
                non-alpha characters in the sequence (used to count stop-codons i promer data). 
                
                An example header might look like: 5198 22885 5389 23089 20 20 0  """

                rstart   = int(ff[0])
                rend     = int(ff[1])
                qstart   = int(ff[2])
                qend     = int(ff[3])

                qstrand  = 1
                hstrand  = 1

                if rend < rstart:
                    qstrand = -1
                else:
                    qstrand = 1

                if qend < qstart:
                    hstrand = -1
                else:
                    hstrand = 1

                #print "Strands %d %d"%(qstrand,hstrand)

                errors   = int(ff[4])
                simerrs  = int(ff[5])
                nonalpha = int(ff[6])
                
                if id1 not in refseqs:
                    raise Exception("Can't find reference sequence [%s] in ref file [%s]"%(id1,args.reffile))

                if id2 not in qryseqs:
                    raise Exception("Can't find query sequence [%s] in query file [%s]"%(id2,args.queryfile))
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


                if (seq1 != seq2  and id1 == "GG739696.1"):
                    print prettyPrint([seq1,seq2])
                
                if id1 not in alns:
                    alns[id1] = []

                tmpgff = Feature()

                tmpgff.qid    = id1
                tmpgff.qstart = rstart
                tmpgff.qend   = rend

                #print "Strand %d %d"%(qstrand,hstrand)

                tmpgff.hitattr['qseq'] = seq1
                tmpgff.hitattr['hseq'] = seq2
                tmpgff.hitattr['hid']  = id1

                tmpgff.hitattr['insertpos'] = insertpos

                #alns[id1].append([seq1,seq2])
                alns[id1].append(tmpgff)

        line = fh.readline()

    
    #for id in alns:
        #print id
        #for gff in alns[id]:
            #print "%s - %s"%( tmpgff.qid,tmpgff.hitattr['hid'])


    gnum = 1

    for id in gffs:
        for g in gffs[id]:

            outstr = []

            name = g.hitattr['Name']
            prod = g.hitattr['product']


            #for h in g.hitattr:
            #    print "%s %s"%(h,g.hitattr[h])

            found    = False
            foundgff = None
            status   = "NEW"

            if id in alns:
                for tmpgff in alns[id]:

                    if g.overlaps(tmpgff):

                        if tmpgff.contains(g):
                            #print "Contained Seq qstart/end %d %d"%(tmpgff.qstart,tmpgff.qend)
                            found    = True
                            foundgff = tmpgff
                        else:

                            ostart = g.qstart
                            oend   = g.qend

                            if tmpgff.qstart > g.qstart:
                                ostart = tmpgff.qstart
                                
                            if tmpgff.qend < g.qend:
                                oend = tmpgff.qend

                            frac = int(100*(oend-ostart+1)/(g.qend-g.qstart+1))

                            status = "PARTALIGN"
                            outstr.append("============1 Processing gene %d %s %s"%(gnum,name,prod))
                            outstr.append("Contig coords from gff file %s %d-%d"%(g.qid,g.qstart,g.qend))
                            outstr.append("Partial overlap of %d percent overlap coords are %d %d"%(frac,ostart,oend))

            
            if not found:
                if status == "NEW":
                    status = "NOALIGN"
                    outstr.append("============2 Processing gene %d %s %s"%(gnum,name,prod))
                    outstr.append("Contig coords from gff file %s %d-%d %s %s"%(g.qid,g.qstart,g.qend,name,prod))
                    outstr.append("ERROR: No align for %s %s qstart/end %d %d %s"%(name,tmpgff.qid,tmpgff.qstart,tmpgff.qend,prod))
            else:
                if qstrand == -1:
                    status = "REVSTRAND"
                    outstr.append("===========3 Processing gene %d %s %s"%(gnum,name,prod))
                    outstr.append("Contig coords from gff file %s %d-%d %s %s"%(g.qid,g.qstart,g.qend,name,prod))
                    outstr.append("ERROR: can't deal with reverse strand reference alignments")
                else:
                    gstrand = g.strand
                    gstart  = g.qstart
                    gend    = g.qend

                    astrand = foundgff.strand
                    astart  = foundgff.qstart
                    aend    = foundgff.qend



                        
                    apos1 = findAlnPos(foundgff,gstart)
                    apos2 = findAlnPos(foundgff,gend)
                        
                        
                    if gstrand == 1:
                        qseq = foundgff.hitattr['qseq']['seq'][apos1:apos2]
                        hseq = foundgff.hitattr['hseq']['seq'][apos1:apos2]
                    else:
                        qseq = foundgff.hitattr['qseq']['seq'][apos1+1:apos2+1]
                        hseq = foundgff.hitattr['hseq']['seq'][apos1+1:apos2+1]
                        
                        qseq = reverse_complement(qseq)
                        hseq = reverse_complement(hseq)

                    

                    if qseq != hseq:
                        status = "MUTATION"
                        outstr.append("===========4 Processing gene %d %s %s"%(gnum,name,prod))


                        #print "GFF %s %s %d %d %s %s"%(g.qid,g.hid,g.qstart,g.qend,name,prod)

                        outstr.append("DNA alignment\n")
                        tmpstr = prettyPrint([{'id': id1, 'seq': qseq},{'id': id2, 'seq': hseq}])
                        tmpff = tmpstr.split('\n')
                        for f in tmpff:
                            outstr.append(f)

                        qpep = translate(qseq)
                        hpep = translate(hseq)

                        tmpstr = prettyPrint([{'id': id1, 'seq': qpep},{'id': id2, 'seq': hpep}])
                        outstr.append("PEP alignment\n")
                        tmpff = tmpstr.split('\n')
                        for f in tmpff:
                            outstr.append(f)




                        #print "GFF start-end strand %d-%d %d %s %s"%(gstart,gend,gstrand,name,prod)
                        #print "ALN start-end strand %d-%d %d %s %s"%(astart,aend,astrand,name,prod)

                        #print "POS %d %d",(apos1,apos2)
                    
                        #print "QSEQ %s"%qseq
                        #print "HSEQ %s"%hseq
                            
                            
                        #print "QPEP %s"%qpep
                        #print "HPEP %s"%hpep
                    else:
                        status = "IDENTICAL"
                        outstr.append("============5 Processing gene %d %s %s"%(gnum,name,prod))
                        outstr.append("NO CHANGE for this alignment %s %s %s"%(tmpgff.qid,name,prod))
        
            for i in outstr:
                print "%-15s %s"%(status,i)
            print "\n"
            gnum = gnum+ 1
        #for (seq1,seq2) in alns[g.qid]:
         #   print "%s - %s"%( seq1['id'],seq2['id'])


def findAlnPos(gff,pos):

    i = 0

    seq1 = gff.hitattr['qseq']['seq']
    seq2 = gff.hitattr['hseq']['seq']
    
    strand = gff.strand
    tmppos = gff.qstart -1

    """ Need to have hpos here """

    while i < len(seq1):

        c1 = seq1[i]
        c2 = seq2[i]

        if c1 != '-':
            tmppos = tmppos + 1
            
        if tmppos == pos:
            return i

        i = i + 1

    return len(seq1)-1

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


def translate(str):

    i = 0

    pep = ""

    while i < len(str)-2:

        codon = str[i:i+3]

        #print "CODON %s"%(codon)

        if codon in standardCodonTable['table']:
            res = standardCodonTable['table'][codon]
        else:
            res = "X"

        #print "RES %s"%res

        pep = pep + res

        i = i + 3

    return pep
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
        else:
            newstr = newstr + ch

        i = i + 1

    return newstr[::-1]

        
if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Convert mummer delta format to fasta')

    parser.add_argument('-d','--deltafile'   , help='The mummer delta output file .delta')
    parser.add_argument('-r','--reffile'     , help="The input reference fasta file")
    parser.add_argument('-q','--queryfile'   , help="The input query fasta file")
    parser.add_argument('-g','--gfffile'     , help="The protein gff file")
    
    args = parser.parse_args()

    main(args)

