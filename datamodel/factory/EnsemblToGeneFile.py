import os
import sys
import os.path
import logging
import importlib
from   config          import settings
from   FileReader      import FileReader
from   datamodel.Feature import Feature

class EnsemblToGeneFile(FileReader):
   
    geneids = {}
    tranids = {}

    def __init__(self,file):
        super(FileReader,self).__init__()

        # Why?  Just why?

        self.filename = file
        self.fh       = open(file)
        self.lnum     = 0
        self.geneids    = {}
	self.tranids    = {}

        
        self.parse()

    def parse(self):
        self.curr_line = FileReader.nextLine(self)

        while self.curr_line:
            if not self.curr_line:
                return

            self.parseLine(self.curr_line)

            self.curr_line = FileReader.nextLine(self)


    def parseLine(self,line):
        line = line.rstrip('\n')
        ff   = line.split('\t')


        #Gm16088 ENSMUST00000160944
        #Gm26206 ENSMUST00000082908
        #Xkr4    ENSMUST00000162897
        #Xkr4    ENSMUST00000159265

        if len(ff) == 2:
            
            geneid = ff[0]
            tranid = ff[1]

            if not self.tranids.has_key(tranid):
                self.tranids[tranid] = {}
                
            if not self.geneids.has_key(geneid):
                self.geneids[geneid] = {}
                

            self.tranids[tranid][geneid] = 1
            self.geneids[geneid][tranid] = 1
                
