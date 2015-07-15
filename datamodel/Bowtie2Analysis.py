from   datamodel.database.DB    import Analysis, AnalysisExpectedOutputFile, AnalysisCommand
from   datamodel.FileUtils      import FileUtils
from   config                   import settings

import os
import re
import logging

class Bowtie2Analysis(Analysis):

    """Class to run bowtie2 against a set of fastq files """

    minimum_space_needed = 1000000000000

    name             = "Bowtie2"
    bowtiebindir     = settings.TOOLDIR  + "bowtie2-2.2.2/"
    bowtiebinname    = "bowtie2"
    bowtiebinfile    = bowtiebindir + bowtiebinname

    samtoolsbindir   = settings.TOOLDIR + "samtools-0.1.19/"
    samtoolsbinname  = "samtools"
    samtoolsbinfile  = samtoolsbindir + samtoolsbinname

    def __init__(self):

        super(Bowtie2Analysis,self).__init__()

    def getCommands(self):

        if self.commands and len(self.commands) >0:
            return self.commands
        
        logging.info(" ========> Analysis %20s Getting commands" % (self.name))

        self.commands              = []
        self.expected_output_files = []
        self.temp_output_files     = []

        outdir = self.output_dir
        tmpdir = self.working_dir

        btbin  = self.bowtiebindir   + self.bowtiebinname
        stbin  = self.samtoolsbindir + self.samtoolsbinname

        self.calculateSpaceNeeded()

        if FileUtils.fileExists(btbin) == False:
            raise Exception("Binary file [%s] doesn't exist = can't continue" % btbin)

        if FileUtils.fileExists(stbin) == False:
            raise Exception("Binary file [%s] doesn't exist = can't continue" % stbin)

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))

        self.checkDiskSpace()

        for fobj in self.input_files:
            f = fobj.input_file
            try:

                if f.endswith(".gz"):
                                                             #  f = "<( zcat -c " + f + " )"
                  tmpf    = f.replace(".gz","")
                  fparts  = FileUtils.getFileParts(tmpf)
                  command = "gunzip -c " + f + " > " + tmpdir + "/" + fparts['basename']
                  self.commands.append(command)
                  self.temp_output_files.append(tmpf)
                  f       = tmpdir + "/" + fparts['basename']

                fparts  = FileUtils.getFileParts(f)
                fstub   = fparts['filestub']

                bowtieoutfile   = tmpdir + "/" + fstub + ".sam"
                samtoolsoutfile = tmpdir + "/" + fstub + ".bam"

                if self.param == None:
                    raise Exception("No parameters entered for bowtie = needs -x <genomeindex>")
                  
                command1 = btbin  + " " + self.param + " " + f + " | " + stbin + " view -bS - | " + stbin + " sort - " + tmpdir + "/" + fstub

                logging.info(" ========> Analysis %20s command 1 : %s" % (self.name,command1))

                #command2 = stbin + " view -bS " + bowtieoutfile + "| " + stbin + " sort - " + tmpdir + "/" + fstub

#                logging.info(" ========> Analysis %20s command 2 : %s" % (self.name,command2))

                command2 = stbin + " index "    + samtoolsoutfile 

                logging.info(" ========> Analysis %20s command 3 : %s" % (self.name,command2))

               # self.expected_output_files.append(fstub + ".sam")
                self.expected_output_files.append(AnalysisExpectedOutputFile(expected_output_file=fstub + ".bam"))
                self.expected_output_files.append(AnalysisExpectedOutputFile(expected_output_file=fstub + ".bam.bai"))
                
                self.commands.append(AnalysisCommand(command=command1))
                self.commands.append(AnalysisCommand(command=command2))
                #self.commands.append(command3)
                
            except Exception as e:
                logging.info(" ========> Analysis %20s Failed building command list [%s]"%(self.name,e))
                raise
                
        return self.commands

    def postProcessOutput(self):
        super(Bowtie2Analysis,self).postProcessOutput()

        #3 reads; of these:
        #  3 (100.00%) were unpaired; of these:
        #    3 (100.00%) aligned 0 times
        #    0 (0.00%) aligned exactly 1 time
        #    0 (0.00%) aligned >1 times
        #  0.00% overall alignment rate

        tmpdat = {}
        
        for str1obj in self.output_strings:
            str1 = str1obj.output_string
            tmpstr = str1.split("\n")

            for str in tmpstr:
                match1 = re.match('(\d+) reads',str)      
                match2 = re.match(' +(\d+) (.*?) aligned 0 times',str)
                match3 = re.match(' +(\d+) (.*?) aligned exactly 1 time',str)
                match4 = re.match(' +(\d+) (.*?) aligned >1 times',str)
                match5 = re.match('(.*) overall alignment rate',str)
                
                if match1:
                    tmpdat['Number_of_Reads']                = match1.group(1)
                    
                if match2:
                    tmpdat['Aligned 0 Times']                = match2.group(1)
                    tmpdat['Percent Aligned 0 Times']        = match2.group(2)
                    
                if match3:
                    tmpdat['Aligned Exactly 1 Time']         = match3.group(1)
                    tmpdat['Percent Aligned Exactly 1 Time'] = match3.group(2)
                    
                if match4:
                    tmpdat['Aligned >1 Time']                = match4.group(1)
                    tmpdat['Percent Aligned >1 Time']        = match4.group(1)

                if match5:
                    tmpdat['Overall Alignment Rate']         = match5.group(1)


        self.summary_data = tmpdat


    def calculateSpaceNeeded(self):
       
        # Sam size is roughly the size of the input. Bam sizes are smaller

        output_size = 0

        for f in self.input_files:
           output_size += os.path.getsize(f.input_file)

        self.minimum_space_needed = 3*output_size

        return self.minimum_space_needed
