from   datamodel.Analysis       import Analysis
from   datamodel.FileUtils      import FileUtils
from   datamodel.factory.SequenceFactory import SequenceFactory
from   config                   import settings

import os
import re
import logging

class BRH2FastaAnalysis(Analysis):

    """Takes a file of best reciprocal hits and gets the full sequence out for each ortholog set and puts them into a file"""

    name        = "BRH2FastaAnalysis"
    minimum_space_needed =0
    def __init__(self):

        super(BRH2FastaAnalysis,self).__init__(self.name)


    def getCommands(self):

        self.checkDiskSpace()

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))


        orths = self.getOrthologs()

        return self.commands
    
    def postProcessOutput(self):

        super(BRH2FastaAnalysis,self).postProcessOutput()

        self.output_status = "DONE"

        for s in self.output_str:
            print s


    def getOrthologs(self):

        orthfile = self.input_files[0];
        
        print "File %s"%orthfile
        orths   = {}
        species = []

        blastdbs = ["~/Dropbox/Seim/seim/MS69-1","~/Dropbox/Seim/seim/70-100-2010","~/Dropbox/Seim/seim/7_1_58FAA","~/Dropbox/Seim/seim/BL21","~/Dropbox/Seim/seim/MS200-1"]

        
        with open(orthfile) as fp:

         line_num = 1

         for line in fp:
             
             line = line.rstrip('\n')

             ff   = line.split()


             if line_num == 1:
               species = ff
             else:
                 
                 for i,val in enumerate(ff):

                     if i == 0:
                         tmp = val.split('|')
                         
                         filename = tmp[3] + ".fa"
                         print "FILE %s"%filename
                         msafp = open(filename,"w")

                     if i < len(ff)-1:
                         blastdb = blastdbs[i]
                         
                         print "VAL %s :%s"%(blastdb,val)
                         if val != "-":
                             seq = SequenceFactory.getSequenceFromBlastDB(val,blastdb)
                             
                             msafp.write(seq[0])
                             print "SEQ %s"%seq
                 
                 msafp.close()

             line_num = line_num+1


  
             
