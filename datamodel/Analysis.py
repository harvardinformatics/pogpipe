import os
import sys
import shutil
import os.path
import logging

from   datamodel.FileUtils               import FileUtils
from   config                            import settings
from   datamodel.factory.AnalysisFactory import AnalysisFactory

"""  
     Input directory:       Not usally local.  Default is cwd
     Working directory:     Local to the running machine - usually /tmp/
     Output directory:      Where the output will finally rest.  Not usually local.  Default is input directory

     Input files:           Look in input directory for these
     Working output files:  In working directory
     Expected output files: Look in working directory to find these
     Final output files:    In output directory - copied from working directory
"""

class Analysis(object):

    """Base class that stores info about an analysis to be run"""

    def __init__(self,name):

        self.id                    = None                     # The database id if we're storing to a db.  None otherwise

        self.owner                 = None                     # Owner user id
        self.owner_email           = None                     # Owner user email (optional)

        self.current_status        = "NEW"
        self.output_status         = None                     # Status after finishing the command - job could still fail due to output processing

        self.input_files           = []                       # Array of input files - sequences, alignments, vcf
        self.input_types           = []                       # Types of input files - fastq,sam,bam,sortedbam,sortedindexedbam,vcf.  This is free test right now

        self.input_dir             = None                     # Where the input files live - default is cwd
        self.working_dir           = settings.TMPDIR          # Where we store intermediate files
        self.output_dir            = settings.OUTPUT_DIR      # Where we store output files - this shouldn't be tmpdir, especially if we're using slurm

        self.expected_output_files = []                       # What output files do we expect
        self.output_files          = []                       # Names of all the output files
        self.output_types          = []                       # Types of output files,  fastq ,fastq.gz, sam, bam, vcf, R1.fastq, R2,fastq, text

        self.commands              = []                       # The system commands that were run
        self.output_str            = []                       # Stdout strings from the commands
        self.summary_data          = {}                       # Key value pairs that summarize the output - e.g. for viewing on a web page

        self.runtype               = 'local'                  # local, slurm, DBlocal, DBslurm
        self.param                 = None                     # Hash of parameters and values (optional)

        self.queue                 = "informatics_dev"        # Slurm queue to use
        self.slurmid               = -1                       # Job id of the slurm job (should this be an array?)
        self.cores                 = 1                        # How many cores to use when running
        self.mempercore            = 1024                     # Memory per core (slurm)

        self.slurmparams           = {}                       # parameters for slurm submission

        self.date_created          = None                     # Time created.  If stored to the db this is the db timestamp
        self.last_updated          = None                     # Time last updated

        self.setName(name)                                    # Name of the Analysis (FastQC, bwa, bowtie2 etc)

        self.temp_output_files     = []

    def init(self):
        """ Function to set up any analysis specific variables """

    
    def toString(self):

        return AnalysisFactory.toString(self)

    def setName(self,name):
        self.name = name
        return True

    def getResultsLog(self):

        str = "\n================================================================="
        str += "Analysis name %s\n"      % self.name
        str += "Output Status %s\n"      % self.output_status
        str += "Current Status %s\n"     % self.current_status
        str += "Input files %s\n"        % ', '.join(self.input_files)
        str += "Input types %s\n"        % ', '.join(self.input_types)
        str += "Output files %s\n"       % ', '.join(self.output_files)
        str += "Output types %s\n"       % ', '.join(self.output_types)
        str += "Input Directory %s\n"    % self.input_dir
        str += "Working Directory %s\n"  % self.working_dir
        str += "Output Directory %s\n"   % self.output_dir
        str += "Commands %s\n"           % ', '.join(self.commands)

        for key,val in self.summary_data.iteritems():
            str += " - Summary data %20s : %20s\n"%(key,val)

        return str

    def getCommands(self):

        """Constructs and returns the command line to run"""


    def setInputFiles(self,input_files,input_types):

        self.input_files = input_files
        self.input_types = input_types

        logging.info(" ========> Analysis %20s called setInputFiles:  Input File Count %s"%(self.name,len(self.input_files)))
        logging.info(" ========> Analysis %20s called setInputFiles:  Input Files are %s"%(self.name,", ".join(self.input_files)))

        return True

    def getInputFiles(self):
        return self.input_files

    def getOutputFiles(self):
        return self.output_files

    def checkDiskSpace(self):

        bytes = FileUtils.getFreeDiskSpace(self.working_dir) 
        logging.info(" ========> Analysis %20s checked disk space for %s Free space (bytes) %s Needed %s"%(self.name,self.working_dir,bytes,self.minimum_space_needed))

        if self.minimum_space_needed and bytes < self.minimum_space_needed:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.working_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)

        elif bytes < 10000000:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.working_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)


        bytes = FileUtils.getFreeDiskSpace(self.output_dir) 
        logging.info(" ========> Analysis %20s checked disk space for %s Free space (bytes) %s Needed %s"%(self.name,self.output_dir,bytes,self.minimum_space_needed))

        if self.minimum_space_needed and bytes < self.minimum_space_needed:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.output_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)

        elif bytes < 10000000:
            str = "Not enough disk space needed in %s.  Needs %s, available %s"%(self.output_dir,self.minimum_space_needed,bytes)
            logging.info(" ========> Analysis %20s %s"%(self.name,str))
            raise Exception(str)

    def checkInputFiles(self):

        valid = True;

        for i in self.input_files:
            if os.path.isfile(i) == False:
                valid = False

        logging.info(" ========> Analysis %20s called checkInputFiles:  Input Files Valid %s"%(self.name,valid))

        return valid


    def checkExpectedOutputFiles(self):
        working_dir = self.working_dir

        valid = True;

        missing_output_files = []
        found_output_files   = []

        for f in self.expected_output_files:

            if os.path.isfile(os.path.join(working_dir,f)):
                found_output_files.append(os.path.join(working_dir,f))
            else:
                missing_output_files.append(os.path.join(working_dir,f))
                valid = False

        logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Expected count %s"%(self.name,len(self.expected_output_files)))
        logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Expected valid %s"%(self.name,valid))
        logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Missing count  %s"%(self.name,len(missing_output_files)))
        logging.info(" ========> Analysis %20s called checkExpectedOutputFiles: Missing files  %s"%(self.name,", ".join(missing_output_files)))

        self.missing_output_files = missing_output_files
        self.found_output_files   = found_output_files

        return valid

    def setParameters(self,param):
        self.param = param


    def postProcessOutput(self):
        """ Checks expected output files exist in the working directory and copies them over to the output directory """

        logging.info(" ========> Analysis %20s called postProcessOutput:"%(self.name))

        if self.checkExpectedOutputFiles() == False:
            raise Exception("Missing expected output files. Number missing are [%d]"%(len(self.missing_output_files)))

        FileUtils.checkDirExists(self.output_dir)

        tmpfiles = []

        logging.info(" ========> Analysis %20s called postProcessOutput: Moving files from %s to %s "%(self.name,self.working_dir,self.output_dir))
        try:
            for srcfile in self.expected_output_files:

                fullsrcfile = os.path.join(self.working_dir,srcfile)
                destfile    = os.path.join(self.output_dir,srcfile)

                FileUtils.checkDirExistsForFile(destfile)

                res = shutil.move(fullsrcfile,destfile)

                if res == None:
                    res = "OK"
                else:
                    res = "FAILED"

                print "Checking %s"%destfile
                tmpfiles.append(destfile)
                
                logging.info(" ========> Analysis %20s called postProcessOutput: Result of file move for  %s = %s" % (self.name,srcfile,res))

        except Exception as e:
            logging.info(" ========> Analysis %20s file move failed %s"%(self.name,e))
            raise

        self.output_files = tmpfiles

        for f in self.temp_output_files:
            logging.info(" ========> Analysis %20s removing temp file %s "%(self.name,f))
	    res = os.remove(f) 

    """ 

    File, directory and disk usage methods 


    """

    def setWorkingDirectory(self,working_dir):
        self.working_dir = working_dir

    def getWorkingDirectory(self):
        return self.working_dir

    def setInputDirectory(self,intput_dir):
        self.input_dir = input_dir

    def getInputDirectory(self):
        return self.input_dir

    def setOutputDirectory(self,output_dir):
        self.output_dir = output_dir

    def getOutputDirectory(self):
        return self.output_dir

    def checkBinary(self,binfile):
        return FileUtils.fileExists(binfile)

