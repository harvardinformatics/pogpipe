import os
import sys
import os.path
import logging
import importlib
from   config          import settings
from   FileReader      import FileReader
from   datamodel.Feature import Feature

class GTFFile(FileReader):
   
    genes = {}

    def __init__(self,file):
        super(FileReader,self).__init__()

        # Why?  Just why?

        self.filename = file
        self.fh       = open(file)
        self.lnum     = 0
        self.genes    = {}

        self.curr_line   = FileReader.nextLine(self)

        self.curr_geneid = None
        self.curr_feat   = None
        self.curr_gene   = None

    def parse(self):

        line = self.curr_line

        while self.curr_line:
            if not self.curr_line:
                return

            feat = self.parseLine(self.curr_line)

            self.addFeature(feat)

            self.curr_line = self.nextLine()


    def nextGene(self):

        if not self.curr_line:
            tmpgene = self.curr_gene
            self.curr_gene = None
            return tmpgene

        while self.curr_line:

            feat = self.parseLine(self.curr_line)

            self.addFeature(feat)

            #print "CCCC %s %s"%(self.curr_geneid,feat.hid)

            tmpid = self.curr_geneid
            
            self.curr_feat   = feat
            self.curr_geneid = feat.hitattr['gene_id']
            self.curr_gene   = self.genes[self.curr_geneid]
            self.curr_line = FileReader.nextLine(self)

#            print "Got feat %s [%s]"%(feat.hid,self.curr_geneid)
            if tmpid and feat.hitattr['gene_id'] != tmpid:
                return tmpid


    def addFeature(self,feat):

        gene_id = None
        transcript_id = None
        gene_name = None

        if 'gene_id' in feat.hitattr:
            gene_id = feat.hitattr['gene_id']

        if 'transcript_id' in feat.hitattr:
            transcript_id = feat.hitattr['transcript_id']

        if 'gene_name' in feat.hitattr:
            gene_name = feat.hitattr['gene_name']

        if gene_id and gene_id not in self.genes.keys():
            self.genes[gene_id] = {}

        if transcript_id and transcript_id not in self.genes[gene_id]:
            self.genes[gene_id][transcript_id] = []

            
        self.genes[gene_id][transcript_id].append(feat)
            

    def getLongestTranscript(self,geneid):
        trans = self.genes[geneid]

        # raise exception here

        maxlen = -1
        maxtransid = None

        for tranid in trans:
            tlen = 0

            for ex in trans[tranid]:
                if ex.type2 == "exon":
                    tlen += ex.qend-ex.qstart+1

            if tlen > maxlen:
                maxlen = tlen
                maxtransid = tranid

        return maxtransid

    def parseLine(self,line):
        line = line.rstrip('\n')
        ff = line.split('\t')

        #chr1	unknown	CDS	3054734	3054733	.	+	-1	gene_id "ENSMUSG00000090025"; gene_name "ENSMUSG00000090025"; transcript_id "ENSMUST00000160944";

        f = Feature()

        f.qid   = ff[0]
        f.type1 = ff[1]
        f.type2 = ff[2]

        f.qstart = int(ff[3])
        f.qend   = int(ff[4])

        if ff[5] != ".":
            f.score = double(ff[5])

        if ff[6] != ".":
            if ff[6] == "+":
                f.strand = 1
            elif ff[6] == 1:
                f.strand = 1
            elif ff[6] == "-":
                f.strand = -1
            elif ff[6] == -1:
                f.strand = -1

        if ff[7] != ".":
            f.phase = int(ff[7])


        featf = ff[8].split(';')
            
        for feat in featf:
            feat = feat.strip()
            tmp  = feat.split(' ')

            if len(tmp) == 2:

                key = tmp[0].strip()
                val = tmp[1].strip()
                val = val.strip('"')

                f.hitattr[key] = val

                if key == "transcript_id":
                    f.hid = val
        return f
