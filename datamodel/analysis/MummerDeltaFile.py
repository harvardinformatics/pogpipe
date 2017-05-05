
from   datamodel.FileUtils      import FileUtils
from   datamodel.Feature        import Feature
from   datamodel.SeqUtils       import SeqUtils
from   subprocess               import Popen, PIPE
from   config                   import settings

import os
import re
import logging


"""

This is what a delta file might look like.  It is generated from the nucmer command which looks like

nucmer --
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

class MummerDeltaFile():

    deltafile  = None
    refseqs    = None
    qryseqs    = None

    alns      = {}

    def __init__(self,deltafile,refseqs,qryseqs):

        self.deltafile = deltafile

        self.refseqs    = refseqs
        self.qryseqs    = qryseqs


        if not FileUtils.fileExists(self.deltafile):
            raise Exception("Can't parse Mummer delta file.  File [%s] doesn't exist"%self.deltafile)


    def parse(self):

        fh = open(self.deltafile)

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

                self.parseLine1(ff)

            elif lnum == 2:

                self.parseLine2(ff)

            else:


                if ff[0].startswith(">"):

                    (id1,id2,len1,len2) = self.parseFastaHeaderLine(ff)

                else:

                    #(id2 == "13397" or id2 == "13398"):
                    #if id1 == "10358" and (id2 == "264854" or id2 == "9742") : 
                    #if id1 == "10358" and (id2 == "13398" or id2 == "13397") : 
                    if id1 == "10358" and (id2 == "10359" or id2 == "10358") : 
                        (rstart,rend,rstrand,qstart,qend,qstrand,errors,simerrs,nonalpha) = self.parseAlignmentHeaderLine(ff)

                        #if rstart == 121113:
                        print "RSTART %d %d"%(rstart,rend)

                        (rseq,qseq) = self.getSequences(id1,id2)


                        (tmprseq,tmpqseq,insertpos) = self.readAlignmentChunk(fh,rstart,rend,qstart,qend,rseq,qseq,rstrand,qstrand)


                        tmpgff = self.createAlignmentGFF(id1,id2,rstart,rend,qstart,qend,rstrand,qstrand,tmprseq,tmpqseq,insertpos)
                
                        if id1 not in self.alns:
                            self.alns[id1] = []

                        self.alns[id1].append(tmpgff)

            line = fh.readline()


    def parseLine1(self,fields):

        """  The first line lists the two original input files separated by a space."""

        print fields
        self.input_file1 = fields[0]
        self.input_file2 = fields[1]

    def parseLine2(self,fields):

        """ The second line specifies the alignment data type, either NUCMER or "PROMER"""

        self.alntype = fields[0]
                
        if self.alntype != "NUCMER":
            raise Exception("Only NUCMER alignments are currently parsed - we have [%s]"%self.alntype)

    def parseFastaHeaderLine(self,fields):

        """ Every grouping of alignment regions have a header, just like the cluster's header in the .cluster file. 
        This is a FASTA style header and lists the two sequences that produced the following alignments after a '>' and separated by a space.
        After the two sequences are the lengths of those sequences in the same order. 
        
        An example header might look like: >tagA1 tagB1 500 2000000   """

        id1 = fields[0].replace(">",'')
        id2 = fields[1]
                
        len1 = int(fields[2])
        len2 = int(fields[3])

        return id1,id2,len1,len2

    def parseAlignmentHeaderLine(self,fields):

        """ The four digits are the start and end in the reference sequence respectively and the start and end in the query sequence respectively. 
        
        These coordinates are always measured in DNA bases regardless of the alignment data type. 
        
        The three digits after the starts and stops are: 
        the number of errors (non-identities), 
        similarity errors (non- positive match scores) 
        non-alpha characters in the sequence (used to count stop-codons i promer data). 
        
        An example header might look like: 5198 22885 5389 23089 20 20 0  """
        
        rstart   = int(fields[0])
        rend     = int(fields[1])
        qstart   = int(fields[2])
        qend     = int(fields[3])
        
        rstrand  = 1
        qstrand  = 1
        
        if rend < rstart:
            rstrand = -1
        else:
            rstrand = 1
            
        if qend < qstart:
            qstrand = -1
        else:
            qstrand = 1
                
        errors   = int(fields[4])
        simerrs  = int(fields[5])
        nonalpha = int(fields[6])

        return rstart,rend,rstrand,qstart,qend,qstrand,errors,simerrs,nonalpha

    def getSequences(self,id1,id2):
        #print "Getting id1 %s from refseqs id2 %s from qseqs"%(id1,id2)
        #print self.qryseqs.keys()
        if id1 not in self.refseqs:
            raise Exception("Can't find reference sequence [%s] in input file [%s]"%(id1,self.input_file1))

        if id2 not in self.qryseqs:
            raise Exception("Can't find query sequence [%s] in input file [%s]"%(id2,self.input_file2))


        rseq = self.refseqs[id1]
        qseq = self.qryseqs[id2]

        return rseq,qseq

    def readAlignmentChunk(self,fh,rstart,rend,qstart,qend,rseq,qseq,rstrand,qstrand):
        """ Each of the alignment headers is followed by a string of signed digits, one per line, with the final line before the next header equaling 0 (zero). 

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
            tmprseq = SeqUtils.reverseComplement(tmprseq)


        if qend > qstart:
            tmpqseq = tmpqseq[qstart-1:qend-1]
        else:
            tmpqseq = tmpqseq[qend:qstart]
            tmpqseq = SeqUtils.reverseComplement(tmpqseq)

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

        return tmprseq,tmpqseq,insertpos

    def createAlignmentGFF(self,id1,id2,rstart,rend,qstart,qend,rstrand,qstrand,tmprseq,tmpqseq,insertpos):
        seq1 = {}
        seq2 = {}

        seq1['id'] = id1
        seq2['id'] = id2

        seq1['seq'] = tmprseq
        seq2['seq'] = tmpqseq

        tmpgff = Feature()
        
        tmpgff.qid    = id1
        tmpgff.qstart = rstart
        tmpgff.qend   = rend
        
        tmpgff.hitattr['qseq'] = seq1
        tmpgff.hitattr['hseq'] = seq2
        tmpgff.hitattr['hid']  = id1

        tmpgff.hitattr['insertpos'] = insertpos

        return tmpgff


    
