from   datamodel.Analysis                import Analysis
from   datamodel.SamtoolsMpileupAnalysis import SamtoolsMpileupAnalysis
from   datamodel.factory.AnalysisFactory import AnalysisFactory
from   datamodel.FileUtils               import FileUtils
from   datamodel.factory.FastaFile       import FastaFile
from   config                            import settings

import os
import re
import logging

from   datamodel.database.DB             import AnalysisCommand

class ParallelMpileupAnalysis(Analysis):

    """Class that runs multiple mpileup on a bam file.  Needs a reference genome fasta file"""

    minimum_space_needed = 10000000

    name         = "ParallelMpileup"
    sub_analyses = []
    chunk        = 1000000

    def __init__(self):

        super(ParallelMpileupAnalysis,self).__init__(self.name)

    def getCommands(self):
        self.commands = []
        self.output_files = []

        self.checkDiskSpace()

        print "Reading genome file"
        seqs = FastaFile.getSequenceDict(self.refgenome,False)

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))


        fileparts = FileUtils.getFileParts(self.input_files[0])

        self.basename = fileparts['basename']

        for seq in seqs:

            len =  seqs[seq]['len']
        
            i = 1

            while i < len:
                end = i + self.chunk -1

                if end > len:
                    end = len

                regionstr = "%s:%d-%d"%(seq,i,end)

                tmpana = AnalysisFactory.createAnalysisFromModuleName("SamtoolsMpileup")

                tmpana.setInputFiles(self.input_files,self.input_types)

                tmpana.refgenome = self.refgenome
                tmpana.regionstr = regionstr
                tmpana.init()

                tmpcmds = tmpana.getCommands()

                for cmd in tmpcmds:
                    self.commands.append(cmd)

                i = i + self.chunk

        return self.commands
    
    def postProcessOutput(self):

        super(ParallelMpileupAnalysis,self).postProcessOutput()

        print self.output_strings
        # Do some checks here - files exist

        #tmpdat = {}
        
        #self.summary_data  = tmpdat
        self.output_status = "DONE"

        for s in self.output_str:
            print s

        #status = output_dat['Basic Statistics']['status']

