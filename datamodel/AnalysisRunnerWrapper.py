import logging
import os
import sys
import csv
import pprint

from   config                              import settings
from   datamodel.AnalysisRunner            import AnalysisRunner
from   datamodel.factory.AnalysisFactory   import AnalysisFactory
from   datamodel.factory.AnalysisDBFactory import AnalysisDBFactory


# If register then
#   -  Job analysis is created and saved to the db.
#   
# If register and slurm then
#   -  Job analysis is created and saved to the db
#   -  SlurmJob is created, batch script created, saved to the db (need new table) and submitted
#   -  Slurm jobid is saved to the db.

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
# python datamodel/AnalysisRunnerWrapper.py -a <analysisid>

# 
class AnalysisRunnerWrapper(object):

    def __init__(self,args):
        
        self.args   = args;
        self.dbobj  = AnalysisDBFactory(settings.DBNAME)

        logging.info("\n\nGot new analysis to run %30s\n\n"  % args.analysis);

        logging.info("%30s %15s is %20s"             % (args.analysis,"analysis",  args.analysis));
        logging.info("%30s %15s is %20s"             % (args.analysis,"input",     args.input));
        logging.info("%30s %15s is %20s"             % (args.analysis,"input_type", args.input_type));
        logging.info("%30s %15s is %20s"             % (args.analysis,"outdir",    args.outdir));
        logging.info("%30s %15s is %20s"             % (args.analysis,"param",     args.param));
        logging.info("%30s %15s is %20s"             % (args.analysis,"runtype",   args.runtype));
        logging.info("%30s %15s is %20s"             % (args.analysis,"queue",     args.queue));
        logging.info("%30s %15s is %20s"             % (args.analysis,"cores",     args.cores));
        logging.info("%30s %15s is %20s"             % (args.analysis,"mempercore",args.mempercore));


    def fetchLaunchableJobIDs(self,numjobs,analysis):

        self.dbfactory = AnalysisDBFactory(settings.DBNAME)

        return self.dbfactory.fetchLaunchableJobIDs(numjobs,analysis)

    def createAnalysisRunnerClassFromID(self,jobid):

        self.dbfactory = AnalysisDBFactory(settings.DBNAME)

        self.ana     = self.dbfactory.fetchAnalysisByID(jobid)

        logging.info("ANA FROM DB %s"%self.ana)

        self.ana.status = "LOADED_FROM_DB"
        self.dbfactory.saveAnalysis(self.ana)


    def createAnalysisRunnerClass(self):

        self.dbfactory = AnalysisDBFactory(settings.DBNAME)

        self.ana     = AnalysisFactory.createAnalysisFromModuleName(self.args.analysis)

        self.ana.setInputFiles     (self.args.input,self.args.input_type)

        self.ana.init()

        self.ana.setParameters     (self.args.param)
        self.dbfactory.saveAnalysis(self.ana)

         
    def run(self):

        try:

            # Create the analysis runner which runs the commands and saves the output

            self.runner  = AnalysisRunner(self.ana)    

            self.dbfactory.updateAnalysisStatus(self.ana,"RUNNING")

            # Run the commands

            self.runner.run()

            self.dbfactory.current_status = "RUN_FINISHED"
            self.dbfactory.saveAnalysis(self.ana)

            # Post process the output including copying tmp files to final output directory

            self.dbfactory.updateAnalysisStatus(self.ana,"PROCESSING_OUTPUT")

            self.ana.postProcessOutput()

            self.dbfactory.current_status = "PROCESSED_OUTPUT"
            self.dbfactory.saveAnalysis(self.ana)

            # Set the final status and save the analysis to the db

            self.ana.current_status  = "ANALYSIS_FINISHED"
            self.dbfactory.saveAnalysis(self.ana)
            
        except Exception as e:

            self.ana.current_status = "FAILED"
            self.dbfactory.saveAnalysis(self.ana)
            
            # Need to add error message to the analysis

            str = "AnalysisRunnerWrapper %20s %s Failed %s Inputs were [%s] Params [%s] Error was [%s]" % (self.ana.name,self.ana.id,self.ana.current_status,self.ana.input_files,self.ana.param,e.args[0])
            logging.error(" ========> %s"%str);
            logging.error(" ========> %s"%e);
            print "ERROR: %s"%e
