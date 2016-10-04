import os
import sys
import os.path
import logging
import importlib
from   config          import settings
from   FileReader      import FileReader
from   datamodel.Feature import Feature


class LastzFile(FileReader):
   
    queryfeat  = {}
    targetfeat = {}

    def __init__(self,file):
        super(FileReader,self).__init__()

        self.filename = file
        self.fh       = open(file)
        self.lnum     = 0
        self.queryhits  = {}
        self.targethits = {}

        self.curr_line  = FileReader.nextLine(self)

    def parse(self):

        while self.curr_line:
            self.nextFeature(self)

    def nextFeature(self):

        if not self.curr_line:
            return

        while self.curr_line.startswith("#"):
            self.curr_line = FileReader.nextLine(self)

        line = self.curr_line

        feat = self.parseLine(self.curr_line)

        self.addFeature(feat)

        self.curr_line = FileReader.nextLine(self)
        
        return feat

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
        ff   = line.split('\t')

        ##score  name1   strand1 size1   zstart1 end1    name2   strand2 size2   zstart2 end2    identity        idPct   coverage        covPct
        #12413   98004798        +       1579    278     1520    F27C8.1 -       1482    200     1455    709/1185        59.8%   1255/1482       84.7%
        #15213   98029119        +       1752    526     1572    F27C8.1 -       1482    365     1415    615/1014        60.7%   1050/1482       70.9%
            
        f = Feature()

        qstrand = ff[2]
        hstrand = ff[7]

        qid    = ff[1]
        qlen   = int(ff[3])
        qstart = int(ff[4])
        qend   = int(ff[5])
        hid    = ff[6]
        hlen   = int(ff[8])
        hstart = int(ff[9])
        hend   = int(ff[10])

        f.qid    = qid
        f.type1  = 'lastz'
        f.type2  = 'lastz'
        f.qstart = qstart
        f.qend   = qend

        f.hid    = hid
        f.hstart = hstart
        f.hend   = hend

        f.score = int(ff[0])

        f.qlen  = qlen
        f.hlen  = hlen

        pid = ff[12].replace('%','')
        cov = ff[14].replace('%','')

        f.hitattr['pid'] = float(pid)
        f.hitattr['cov'] = float(cov)

        if qstrand == "+" and hstrand == "+":
            strand = 1
        elif qstrand == "+" and hstrand == "-":
            strand = -1
        elif qstrand == "-" and hstrand == "+":
            strand = -1
        elif qstrand == "-" and hstrand == "-":
            strand = 1

        return f
