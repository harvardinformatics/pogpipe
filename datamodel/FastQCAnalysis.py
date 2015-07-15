from   datamodel.database.DB    import Analysis, AnalysisCommand
from   datamodel.FileUtils      import FileUtils
from   config                   import settings

import os
import re
import logging

class FastQCAnalysis(Analysis):

    """Class that has all the info to run FastQC on fastq files"""

    minimum_space_needed = 1000000

    name       = "FastQC"
    bindir     = settings.TOOLDIR  + "FastQC"
    classpath  = bindir + ":" + bindir + "/sam-1.32.jar:"+bindir+"/jbzip2-0.9.jar"
    binfile    = "java -Xmx1024M -Djava.awt.headless=true -Djava.awt.headlesslib=true -classpath "+classpath + " " + " uk.ac.babraham.FastQC.FastQCApplication"
    fastqc_dir = None

    def __init__(self):

        super(FastQCAnalysis,self).__init__()

        self.expected_output_filelist = ['fastqc_data.txt',
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

        

    """ This is only working with one file - need to work out how to specify number of inputs (input_num?)"""

    def setInputFiles(self,input_files,input_types):
        super(FastQCAnalysis,self).setInputFiles(input_files,input_types)
        
        self.init()
        
    def init(self):
        super(FastQCAnalysis,self).init()
        
        if len(self.input_files) == 0:
            raise Exception("No input files for FastQCAnalysis module. Can't init")

        fileparts = FileUtils.getFileParts(self.input_files[0].input_file)

        if fileparts['fileext'] == ".fastq":
            dir = fileparts['filestub'] + "_fastqc/"
        elif fileparts['fileext'] == ".gz":
            dir = fileparts['filestub'].replace(".fastq","") + "_fastqc/"
        else:
            dir = fileparts['basename'] + "_fastqc/"


        self.fastqc_dir = dir

        tmp = []

        for i,f in enumerate(self.expected_output_filelist):
            #tmp.append(dir + f)
            self.addExpectedOutputFile(dir + f)
            
        #self.expected_output_files = tmp

        
    def getCommands(self):

        self.checkDiskSpace()

        if self.checkInputFiles() == False:
            raise Exception("Input files [%s] don't exist = can't continue"%(self.input_files))

        command = "java -Xmx1024M -Djava.awt.headless=true -Djava.awt.headlesslib=true -classpath " + self.classpath + " " + " -Dfastqc.output_dir=" + self.working_dir + " uk.ac.babraham.FastQC.FastQCApplication " + self.input_files[0].input_file

        self.commands.append(AnalysisCommand(command=command,command_rank=len(self.commands)+1))

        return self.commands
    
    def postProcessOutput(self):

        super(FastQCAnalysis,self).postProcessOutput()

        output_dat = self.readOutputFastqcData()

        encoding  = None
        readlen   = None
        numseqs   = None
        filename  = None
        percentgc = None

        status    = output_dat['Basic Statistics']['status']

        for row in output_dat['Basic Statistics']['moddata']:
            key   = row[0]
            value = row[1]

            if key == "Encoding":
                encoding = value
            elif key == "Sequence length":
                readlen = value
            elif key == "Total Sequences":
                numseqs = value
            elif key == "Filename":
                filename = value
            elif key == "%GC":
                percentgc = value

        tmpdat = {}
        
        tmpdat['Encoding']        = encoding
        tmpdat['Sequence Length'] = readlen
        tmpdat['Filename']        = filename
        tmpdat['%GC']             = percentgc
        tmpdat['Total Sequences'] = numseqs
        
        self.summary_data  = tmpdat
        self.output_status = status

        status = output_dat['Basic Statistics']['status']

    def readOutputFastqcData(self):

        """ Data format looks like sets of
        >>Basic Statistics      pass
        #Measure        Value   
        Filename        sample_1.fq     
        File type       Conventional base calls 
        Encoding        Illumina 1.5    
        Total Sequences 750000  
        Filtered Sequences      0       
        Sequence length 36      
        %GC     43      
        >>END_MODULE
        """

        print self.output_dir
        print self.fastqc_dir
        file = os.path.join(self.output_dir,self.fastqc_dir)
        print "File %s"%file
        file = os.path.join(file,"fastqc_data.txt")
        print "File %s"%file

        data   = {}
        name   = None

        in_data_section = False

        with open(file) as fp:

            for line in fp:

                line = line.rstrip('\n')

                match1 = re.match('\>\>(.*)',line)               # Look for an end line

                if match1:

                    tmpstr = match1.group(1)

                    if tmpstr == "END_MODULE":                   
                    
                        in_data_section = False

                        name   = None
                        status = None

                match2 = re.match('\>\>(.*)\t(.*)',line)        # Look for a start line

                if match2:                                       
                    name    = match2.group(1)
                    status  = match2.group(2)
                    
                    in_data_section = True
                    
                    data[name] = {}
                    data[name]['status'] = status
                    data[name]['moddata']   = []

                else:
                    if in_data_section:                         # Read data line otherwise

                        # If we start with hash then we have a header
                    
                        match3 = re.match('^#(.*)',line)

                        if match3:

                            tmpstr = match3.group(1)
                            header = tmpstr.split('\t')
                            
                            data[name]['header'] = header
                            
                        else :      
                            moddata = line.split('\t')
                            data[name]['moddata'].append(moddata)
        return data
                    
