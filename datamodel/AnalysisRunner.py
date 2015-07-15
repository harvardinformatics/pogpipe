import os
import sys
import os.path
import logging

from   subprocess                  import Popen, PIPE
from   datamodel.database.DB       import Analysis
from   config                      import settings
from   datamodel.database.AnalysisUtils import AnalysisUtils
# Checking executable bit on binaries
# Adding output directory as well as working directory
# Ability to get input file stub/dir
# Post-process output
# Cleanup
# Check dir exists - overwrite

class AnalysisRunner(object):

    """Base class that takes input, runs a command and returns output"""
    
    def __init__(self,analysis):

        self.analysis = analysis

    def run(self):

        logging.info(" ========> AnalysisRunner for %20s called run"%(self.analysis.name))

        self.analysis.output_strings = []

        # We may want to put the output into an array for multiple commands.

        cmds = self.analysis.getCommands()

        logging.info(" ========> AnalysisRunner for %20s called run for %s commands"%(self.analysis.name,len(self.analysis.commands)))

        for cmdobj in cmds:
            cmd = cmdobj.command
            logging.info(" ========> AnalysisRunner for %20s running comand %s"%(self.analysis.name,cmd))

            # Open a pipe

            p = Popen([cmd], 
                      shell     = True, 
                      stdout    = PIPE,
                      stderr    = PIPE,
                      close_fds = True)

            # Loop over the output - Johnny B likely has something to say about this

            while p.poll() == None:

                (out,err) = p.communicate()

                #print "OUT - %s"%out
                #print "ERR - %s"%err

                if out != '':
                    AnalysisUtils.addOutputString(self.analysis,out)
                    sys.stdout.flush()

                if err != '':
                    AnalysisUtils.addOutputString(self.analysis,err)
                    sys.stderr.flush()

        logging.info(" ========> AnalysisRunner for %20s finished command: Output is"%(self.analysis.name))

        for tmp in self.analysis.output_strings:
            tmp2 = tmp.output_string.split("\n")

            for t in tmp2:
                logging.info(" ========> Analysis %20s Output %s"%(self.analysis.name,t))

        return True


