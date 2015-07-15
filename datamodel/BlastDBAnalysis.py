from   datamodel.Analysis       import Analysis
from   datamodel.FileUtils      import FileUtils
from   config                   import settings

import os
import re
import logging

class BlastDBAnalysis(Analysis):

    """Class that has all the info to run FastQC on fastq files"""

    minimum_space_needed = 1000000

    name        = "BlastDB"
    bindir      = settings.TOOLDIR  + "/ncbi-blast-2.2.30+/bin/"
    progname    = "makeblastdb"
    makeblastdb = bindir + progname

    def __init__(self):

        super(BlastDBAnalysis,self).__init__(self.name)


    def getCommands(self):

        self.checkDiskSpace()

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))


        fileparts = FileUtils.getFileParts(self.input_files[0])

        self.basename = fileparts['basename']

        # Need to set dbtype somewhere

        command = self.makeblastdb + " -in " + self.input_files[0] + " -input_type fasta -dbtype prot -title " + self.basename + " -parse_seqids -out " + fileparts['dirname'] + "/" + self.basename

        print "Command %s"%command

        self.commands.append(command)

        return self.commands
    
    def postProcessOutput(self):

        super(BlastDBAnalysis,self).postProcessOutput()

        # Do some checks here - files exist

        #tmpdat = {}
        
        #self.summary_data  = tmpdat
        self.output_status = "DONE"

        for s in self.output_str:
            print s

        #status = output_dat['Basic Statistics']['status']

