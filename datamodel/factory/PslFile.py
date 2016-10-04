import os
import sys
import os.path
import logging
import importlib
from   config          import settings
from   FileReader      import FileReader
from   datamodel.Feature import Feature


class PslFile(FileReader):
   
    queryfeat  = {}
    targetfeat = {}

    def __init__(self,file):
        super(FileReader,self).__init__()

        self.filename = file
        self.fh       = open(file)
        self.lnum     = 0
        self.queryhits = {}
        self.targethits = {}

        while self.lnum < 6:
            self.lnum = self.lnum + 1
            self.curr_line = FileReader.nextLine(self)

    def parse(self):

        line = self.curr_line

        while self.curr_line:
            if not self.curr_line:
                return

            feat = self.parseLine(self.curr_line)

            self.addFeature(feat)

            self.curr_line = self.nextLine(self)


    def addFeature(self,feat):

        qid = feat.qid
        hid = feat.hid

        if qid not in self.queryfeat:
            self.queryfeat[qid] = []

        if hid not in self.targetfeat:
            self.targetfeat[hid] = []

        self.queryfeat[qid].append(feat)
        self.targetfeat[hid].append(feat)

    def parseLine(self,line):
        line = line.rstrip('\n')
        ff = line.split('\t')

        #psLayout version 3

        #match	mis- 	rep. 	N's	Q gap	Q gap	T gap	T gap	strand	Q        	Q   	Q    	Q  	T        	T   	T    	T  	block	blockSizes 	qStart	 tStarts
     	#match	match	   	count	bases	count	bases	      	name     	size	start	end	name     	size	start	end	count
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------
        #236	0	0	0	0	0	0	0	+	TRINITY_DN4669_c0_g1_i1	237	0	236	Gm16144_ENSMUST00000131093	1843	1272	1508	1	236,	0,	1272,
        #179	0	0	0	0	0	0	0	-	TRINITY_DN4615_c0_g1_i1	317	0	179	Hdhd3_ENSMUST00000037820	2977	0	179	1	179,	138,	0,
        #183	0	0	0	0	0	0	0	+	TRINITY_DN4601_c0_g1_i1	219	36	219	Atp6v1a_ENSMUST00000130036	40052	2211	2394	1

            
        f = Feature()

        match  = ff[0]
        strand = ff[1]
        qid    = ff[9]
        qlen   = int(ff[10])
        qstart = int(ff[11])
        qend   = int(ff[12])
        hid    = ff[13]
        hlen   = int(ff[14])
        hstart = int(ff[15])
        hend   = int(ff[16])

        f.qid    = qid
        f.type1  = 'blat'
        f.type2  = 'blat'
        f.qstart = qstart
        f.qend   = qend

        f.hid    = hid
        f.hstart = hstart
        f.hend   = hend

        f.score = int(100*match/qlen)

        if strand != ".":
            if strand == "+":
                f.strand = 1
            elif strand == 1:
                f.strand = 1
            elif strand == "-":
                f.strand = -1
            elif strand  == -1:
                f.strand = -1

        return f
