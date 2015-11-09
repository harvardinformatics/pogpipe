from   datamodel.Analysis          import Analysis
from   datamodel.FileUtils         import FileUtils
from   datamodel.factory.FastaFile import FastaFile
from   config                      import settings

import os
import re
import logging

from   datamodel.database.DB             import AnalysisCommand


# Input multiple bams

# Output slurm commands


class SamtoolsMpileupAnalysis(Analysis):

    """Class that runs samtools mpileup on a bam file.  Needs a reference genome fasta file"""

    minimum_space_needed = 10000000

    name        = "SamtoolsMpileup"
    bindir      = settings.TOOLDIR  + "/samtools-0.1.19/"
    progname    = "samtools"
    samtools    = bindir + progname
    bcftools    = bindir + "/bcftools/bcftools"
    vcfutils    = bindir + "/bcftools/vcfutils.pl"

    regionstr   = ""

    def __init__(self):

        super(SamtoolsMpileupAnalysis,self).__init__(self.name)


    
    def getCommands(self):
        self.commands = []
        self.output_files = []

        self.checkDiskSpace()

        seqs = FastaFile.getSequenceDict(self.refgenome,False)

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))

        fileparts = FileUtils.getFileParts(self.input_files[0])

        self.basename = fileparts['basename']

        # Need to set dbtype somewhere

        outfile1 = self.working_dir + "/" + self.basename + ".raw.vcf"
        outfile2 = self.working_dir + "/" + self.basename + ".flt.vcf"

        regstr = ""

        if self.regionstr != "":
            regstr = " -r " + self.regionstr
            outfile1 = self.working_dir + "/" + self.basename + "." + self.regionstr + ".raw.vcf"
            outfile2 = self.working_dir + "/" + self.basename + "." + self.regionstr + ".flt.vcf"

        

        self.expected_output_files.append(outfile1)
        self.expected_output_files.append(outfile2)

        command1 = self.samtools + " mpileup -uf " + self.refgenome + " " +  self.input_files[0] +  " " + regstr + " | " +                                          self.bcftools + " view " +   " -bvcg -  > " + outfile1                     

        command2 = self.bcftools + " view " + outfile1 + " | " + self.vcfutils + " varFilter -D100 > " + outfile2

        print "Command %s"%command1
        print "Command %s"%command2

        self.commands.append(AnalysisCommand(command=command1,command_rank=len(self.commands)+1))
        self.commands.append(AnalysisCommand(command=command2,command_rank=len(self.commands)+1))


        return self.commands
    
    def postProcessOutput(self):

        super(SamtoolsMpileupAnalysis,self).postProcessOutput()

        print self.output_strings
        # Do some checks here - files exist

        #tmpdat = {}
        
        #self.summary_data  = tmpdat
        self.output_status = "DONE"

        for s in self.output_str:
            print s

        #status = output_dat['Basic Statistics']['status']

