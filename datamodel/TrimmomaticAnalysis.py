from   datamodel.Analysis       import Analysis
from   config                   import settings

import os
import logging

class TrimmomaticAnalysis(Analysis):

    """Class that runs Trimmomatic on fastq files"""

    name    = "Trimmomatic"
    bindir  = settings.TOOLDIR  + "Trimmomatic-0.32"
    binname = "trimmomatic-0.32.jar"
    cores   = 1

    def __init__(self):

        super(TrimmomaticAnalysisRunner,self).__init__()

        self.expected_output_files = ['fastqc_data.txt',
                                 'summary.txt',
                                 'fastqc_report.html',
                                 'Images/duplication_levels.png',
                                 'Images/per_base_gc_content.png',
                                 'Images/per_base_n_content.png',
                                 'Images/per_base_quality.png',
                                 'Images/per_base_sequence_content.png',
                                 'Images/per_sequence_gc_content.png',
                                 'Images/per_sequence_quality.png',
                                 'Images/sequence_length_distribution.png',
                                 ]


    def checkBinary(self):
        jarfile = self.bindir + "/" + 
        binfile = self.bindir + "/" + self.binname
        
        return self.fileExists(binfile)

    def getCommands(self):
        cmds = []

        logging.info(" - In getCommands %s" % self.input)

        if self.checkBinary() and self.checkInputs():

            fileparts = self.getFileParts(self.input[0])
        
            cmd = "java -jar " self.binfile + " -outdir " + self.getWorkingDirectory() + " " + self.input[0]

            print cmd

            cmds.append(cmd)

        else:
            raise Exception('Binary [%s/%s]and/or inputs [%s] don\'t pass checks for %s' % (self.bindir,self.binname,self.input,self.name))

        print cmds
        return cmds

    
    def postProcessOutput(self):

        super(FastQCAnalysisRunner,self).postProcessOutput()

        
