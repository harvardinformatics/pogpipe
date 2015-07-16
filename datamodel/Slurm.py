import re
import os
import sys
import logging

from   subprocess                          import Popen, PIPE

from   config                              import settings
from   datamodel.Analysis                  import Analysis
from   datamodel.FileUtils                 import FileUtils

# Contents of slurm script
#
# #!/usr/bin/env bash
# #SBATCH -J myRjob <- the analysis number
# #SBATCH -o myRjob_slurm.out   <- full path here
# #SBATCH -e myRjob_slurm.err   <- full path here
# #SBATCH -p informatics-dev    <- queue from analysis
# #SBATCH -n 1                  <- number of cores?
# #SBATCH -t 5                  <- time in minutes 
# #SBATCH --mem=100             <- memory in Mb
#

""" Class that creates, saves and submits slurm jobs """

class Slurm(object):

    analysis = None

    def __init__(self,analysis):
        
        self.setAnalysis(analysis)

    def setAnalysis(self,analysis):

        self.analysis = analysis

    def createSbatchFile(self):

        # Create batch file in working directory
        # From analysis get :

        #   queue
        #   expected memory
        #   number of cores
        #   time to allocate

        cwd  = self.analysis.output_dir
        name = self.analysis.name

        self.batchfile = FileUtils.getDatestampedFilename(cwd,
                                                          "PogPipe."+name,
                                                          ".sbatch")
        jobname = "PogPipe." + name

        jobout  = os.path.join(cwd,jobname+".out")
        joberr  = os.path.join(cwd,jobname+".err")

        queue        = self.analysis.queue
        cores        = self.analysis.cores
        mempercore   = self.analysis.mempercore
        time         = "120"

        
        # Contents of slurm script is something like
        #
        # #!/usr/bin/env bash
        # #SBATCH -J myRjob <- the analysis number
        # #SBATCH -o myRjob_slurm.out   <- full path here
        # #SBATCH -e myRjob_slurm.err   <- full path here
        # #SBATCH -p informatics-dev    <- queue from analysis
        # #SBATCH -n 1                  <- number of cores?
        # #SBATCH -t 5                  <- time in minutes 
        # #SBATCH --mem=100             <- memory in Mb

    
        str  = "#!/usr/bin/env bash\n"
        str += "#SBATCH =J " + jobname +"\n"
        str += "#SBATCH -o " + jobout  +"\n"
        str += "#SBATCH -e " + joberr  +"\n"
        str += "#SBATCH -p " + queue   +"\n"
        str += "#SBATCH -n %d" % (cores) +"\n"
        str += "#SBATCH -t %s" % (time)  +"\n"
        str += "#SBATCH --mem=%d" % (mempercore)  +"\n"


        # If we have an analysis id we're reading from the db.  If not then we're on the command line

        if self.analysis.id is None:
            str += "python " + settings.POGPIPEROOT + "bin/run_analysis.py -a " + name + " -i "
 
            str += self.analysis.input_files[0].input_file
    
        else:
            str += "python " + settings.POGPIPEROOT + "bin/run_analysis.py -a " + name + " -i "
 
            str += self.analysis.input_files[0].input_file

        self.batchfiletext = str

        FileUtils.writeTextToFile(self.batchfile,str)

    def submitSlurmJob():

        self.slurmSubmitCommand = "sbatch " + self.sbatchfile

        # Submit the job and get the id

        p = Popen([cmd], 
                  shell     = True, 
                  stdout    = PIPE,
                  stderr    = PIPE,
                  close_fds = True)

        while p.poll() == None:
            print "POLL"

            (out,err) = p.communicate()

            print "OUT - %s"%out
            print "ERR - %s"%err

            if out != '':
                self.analysis.output_str.append(out)
                print out
                sys.stdout.flush()

            if err != '':
                self.analysis.output_str.append(err)
                print err
                sys.stderr.flush()

        print "OUTPUT %s"%self.analysis.output_str
        print self.analysis
        return True



        id = 1

        self.analysis.slurmid = id
        self.analysis.status  = "SUBMITTED"

        
    # Slurm factory
    #def getSlurmJobStatus():
        

